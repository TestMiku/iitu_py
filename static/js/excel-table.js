$.fn.saveExcelCellValue = function (value) {
  $(this).trigger("save-excel-cell", [value]);
};

$.fn.excelTable = function (options) {
  function css(cell, name, value) {
    const properties = $(cell).data("properties");
    properties.style[name] = value;
    $(cell).css(name, value);
    $(cell).data("properties", properties);
  }

  function onCellFocusIn(cell) {
    notShowNote = true;
    $(cell).css({
      outline: "none",
    });
    onInputStyles(cell);
    value = $(cell).data("value");
    $(cell).html(value);
  }

  async function _saveCell(cell) {
    const type = $(cell).data("type");
    const row = $(cell).parent().data("row");
    const column = $(cell).data("column");
    const properties = $(cell).data("properties");
    const readonly = $(cell).data("readonly");
    let value = $(cell).data("value");
    try {
      if (value) {
        switch (type) {
          case "number":
            value = parseFloat(value);
            break;
        }
      }
      await saveCell(cell, row, column, type, readonly, value, properties);
    } catch (error) {
      console.error("Error when saving this cell", error, cell);
    }
  }

  let value = null;
  async function onCellFocusOut(cell, saveValue = false) {
    if (saveValue) {
      $(cell).data("value", value);
    }
    $(cell).html(valueDisplay(cell));
    onDisplayStyles(cell);
    await _saveCell(cell);
    $(cell).off("focusout", onFocusOut);
    $(cell).prop("contentEditable", "false");
    $(cell).on("focusout", onFocusOut);

    $(cell).css({
      outline: "",
      boxShadow: "",
    });
    hidePropertiesMenu();
    hideContextMenu();
    notShowNote = false;
  }

  async function onFocusOut() {
    await onCellFocusOut(this, true);
  }

  function onDisplayStyles(cell) {
    const type = $(cell).data("type");
    const properties = $(cell).data("properties");
    const css = {};
    if (properties && properties.style) {
      css.textAlign = properties.style.textAlign;
    }
    switch (type) {
      case "number":
        if (!css.textAlign) {
          css.textAlign = "right";
        }
        break;
    }
    $(cell).css(css);
  }

  function getCellNumberFormat(cell) {
    return new Intl.NumberFormat("ru-RU", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
  }

  function valueDisplay(cell) {
    const type = $(cell).data("type");
    const value = $(cell).data("value");
    const numberFormat = getCellNumberFormat(cell);
    switch (type) {
      case "number":
        const number = parseFloat(value);
        return number ? numberFormat.format(number) : "";
      default:
        return value;
    }
  }

  function onInputStyles(cell) {
    const type = $(cell).data("type");
    const css = { textAlign: "left" };
    switch (type) {
      case "number":
        break;
    }
    $(cell).css(css);
  }

  function onInput(cell) {
    value = $(cell).html();
  }

  function showPropertiesMenuRelative(cell) {
    propertiesMenu.appendTo($(cell).offsetParent());
    const position = $(cell).offset();
    position.top -= propertiesMenu.outerHeight() + 4;
    position.left += $(cell).outerWidth() - $(propertiesMenu).outerWidth();
    propertiesMenu.addClass("active");
    propertiesMenu.css(position);
    loadPropertiesFrom(cell);
  }

  function hidePropertiesMenu() {
    propertiesMenu.removeClass("active");
  }

  function showContextMenu(x, y) {
    contextMenu.css({
      left: `${x}px`,
      top: `${y}px`,
      position: "absolute",
      display: "",
    });
    const properties = $(activeCell).data("properties");
    $(".add-note-button", contextMenu).toggleClass("d-none", !!properties.note);
    $(".delete-note-button", contextMenu).toggleClass(
      "d-none",
      !properties.note
    );
    $(".update-note-button", contextMenu).toggleClass(
      "d-none",
      !properties.note
    );
  }

  function hideContextMenu() {
    contextMenu.css({
      display: "none",
    });
  }

  async function onKeyPress(cell, event) {
    const type = $(cell).data("type");
    if (event.which === 13 && (type === "number" || !event.shiftKey)) {
      event.preventDefault();
      await onCellFocusOut(cell, true);
      return;
    }
    switch (type) {
      case "number":
        if (event.which < 48 || event.which > 57) {
          event.preventDefault();
        }
        break;
    }
  }

  async function onClick(cell) {
    if (activeCell && activeCell !== cell) {
      await onCellFocusOut(activeCell);
      $(activeCell).css({
        boxShadow: "",
      });
    }
    $(cell).css({
      boxShadow: "inset 0 0 0 1px rgb(13, 110, 253, 0.5)",
    });
    activeCell = cell;
  }

  function onDblClick(cell) {
    if ($(cell).data("readonly")) return;
    $(cell).prop("contentEditable", "true");
    $(cell).focus();
  }

  const table = this[0];
  if (!table || !(table instanceof HTMLTableElement)) {
    console.error("This is not table", this);
    return;
  }
  const getRows = options.getRows;
  const saveCell = options.saveCell;
  const insertRow = options.insertRow;
  if (!getRows || !saveCell || !insertRow) {
    console.error("Specify getRows, saveCell, insertRow in options for", this);
    return;
  }
  let propertiesMenuSelector = $(table).data("cellPropertiesMenuTarget");
  if (!propertiesMenuSelector) {
    console.error(
      "Specify [data-cell-properties-menu-target] in attributes for",
      this
    );
    return;
  }
  const propertiesMenu = $(propertiesMenuSelector);
  if (propertiesMenu.length === 0) {
    console.error(
      `Element with selector ${propertiesMenuSelector} does not exists`,
      this
    );
    return;
  }

  let activeCell = null;
  $(document).keydown(async function (event) {
    if (event.keyCode == 27 && activeCell) {
      await onCellFocusOut(activeCell);
      activeCell = null;
    }
  });

  const note = $(`
		<div class="note card card-shadow ms-1 mt-1">
			<div class="card-body">
				<h6>Примечание</h6>
				<div class="note-text"></div>
			</div>
		</div>
	`);

  function showNoteRelative(cell) {
    const properties = $(cell).data("properties");
    if (properties.note && !notShowNote) {
      note.addClass("active");
      note.appendTo($(cell).offsetParent());
      const position = $(cell).offset();
      position.left += $(cell).outerWidth();
      $(".note-text", note).text(properties.note);
      note.css(position);
    }
  }

  function hideNote() {
    note.removeClass("active");
  }

  let notShowNote = false;

  const initializedCells = new Set();
  function initializeCell(cell) {
    if (initializedCells.has(cell)) return;
    const type = $(cell).data("type");
    const row = $(cell).parent().data("row");
    const column = $(cell).data("column");
    if (!type || !row || !column) {
      console.error("Specify row, column, type for", cell);
      return;
    }
    $(cell).data("properties", {
      style: {},
    });

    $(cell).css({
      maxWidth: "10em",
      userSelect: "none",
    });
    $(cell).html(valueDisplay(cell));
    initializedCells.add(cell);
  }

  $(this)
    .on("mouseenter", ".excel-cell", function () {
      initializeCell(this);
      showNoteRelative(this);
    })
    .on("mouseleave", ".excel-cell", function () {
      initializeCell(this);
      hideNote();
    })
    .on("keypress", ".excel-cell", async function (event) {
      initializeCell(this);
      await onKeyPress(this, event);
    })
    .on("input", ".excel-cell", async function () {
      initializeCell(this);
      onInput(this);
    })
    .on("click", ".excel-cell", async function () {
      initializeCell(this);
      hidePropertiesMenu();
      hideContextMenu();
      await onClick(this);
    })
    .on("contextmenu", ".excel-cell", async function (event) {
      initializeCell(this);
      event.preventDefault();
      await onClick(this);

      showPropertiesMenuRelative(this);
      showContextMenu(event.pageX, event.pageY);
      notShowNote = true;
      hideNote();
    })
    .on("dblclick", ".excel-cell", function () {
      initializeCell(this);
      onDblClick(this);
      hideNote();
    })
    .on("focusin", ".excel-cell", function () {
      initializeCell(this);
      onCellFocusIn(this);
    })
    .on("focusout", ".excel-cell", async function () {
      initializeCell(this);
      await onCellFocusOut(this, true);
    })
    .on("save-excel-cell", ".excel-cell", async function (event, value) {
      initializeCell(this);
      $(this).data("value", value);
      await _saveCell(this);
    });

  propertiesMenu.on("click", function (event) {
    event.stopPropagation();
  });

  function loadPropertiesFrom(cell) {
    const computedStyle = getComputedStyle(cell);
    const properties = $(cell).data("properties");
    const whiteColors = ["#fff", "white", "#ffffff", "rgb(255, 255, 255)"];
    $(".background-color-auto-btn", propertiesMenu).css(
      "color",
      !backgroundColor || whiteColors.includes(backgroundColor.toLowerCase())
        ? ""
        : backgroundColor
    );
    $(".text-color-auto-btn", propertiesMenu).css(
      "color",
      !textColor || whiteColors.includes(textColor.toLowerCase())
        ? ""
        : textColor
    );
    $(".bold-toggle-button", propertiesMenu).toggleClass(
      "active",
      properties.style.fontWeight === "bold"
    );
    $(".italic-toggle-button", propertiesMenu).toggleClass(
      "active",
      properties.style.fontStyle === "italic"
    );
    $(".underline-toggle-button", propertiesMenu).toggleClass(
      "active",
      (properties.style.textDecoration || "").includes("underline")
    );
    $(".strikethrough-toggle-button", propertiesMenu).toggleClass(
      "active",
      (properties.style.textDecoration || "").includes("line-through")
    );
    let textAlign = properties.style.textAlign;
    if (!textAlign) {
      switch ($(cell).data("type")) {
        case "number":
          textAlign = "right";
          break;

        default:
          textAlign = "left";
          break;
      }
    }
    $(`.text-align-radio[value="${textAlign}"]`, propertiesMenu).prop(
      "checked",
      true
    );

    $(
      `.vertical-align-radio[value="${
        properties.style.verticalAlign || "middle"
      }"]`,
      propertiesMenu
    ).prop("checked", true);

    $(
      `.font-family-select option[value="${
        properties.style.fontFamily || ""
      }"]`,
      propertiesMenu
    );
    $(`.font-size-input`, propertiesMenu).val(
      properties.style.fontSize || parseInt(computedStyle.fontSize)
    );
  }

  let textColor = "black";
  $(".text-color .cell-color-picker", propertiesMenu)
    .on("click", function () {
      if (activeCell) {
        textColor = getComputedStyle(this).backgroundColor;
        css(activeCell, "color", textColor);
        const dropdown = new bootstrap.Dropdown(
          $(".text-color-dropdown", propertiesMenu)[0]
        );
        dropdown.hide();
      }
    })
    .mouseenter(function () {
      if (activeCell) {
        $(activeCell).css("color", getComputedStyle(this).backgroundColor);
      }
    })
    .mouseleave(function () {
      if (activeCell) {
        $(activeCell).css(
          "color",
          $(activeCell).data("properties").style.color || ""
        );
      }
    });

  $(".font-family-select", propertiesMenu).on("change", function () {
    if (activeCell) {
      const fontFamily = $(this).val();
      css(activeCell, "fontFamily", fontFamily);
    }
  });

  $(".font-size-input", propertiesMenu).on("input", function () {
    if (activeCell) {
      const computedStyle = getComputedStyle(activeCell);
      let fontSize = $(this).val()
        ? parseInt($(this).val())
        : parseInt(computedStyle.fontSize);
      if ($(this).prop("max")) {
        fontSize = Math.min(parseInt($(this).prop("max")), fontSize);
      }
      if ($(this).prop("min")) {
        fontSize = Math.max(parseInt($(this).prop("min")), fontSize);
      }
      $(this).val(fontSize);
      css(activeCell, "fontSize", fontSize);
    }
  });

  $(".font-size-increase-button", propertiesMenu).on("click", function () {
    if (activeCell) {
      const computedStyle = getComputedStyle(activeCell);
      const fontSizeInput = $(".font-size-input", propertiesMenu);
      let fontSize = fontSizeInput.val()
        ? parseInt(fontSizeInput.val()) + 1
        : parseInt(computedStyle.fontSize);
      if (fontSizeInput.prop("max")) {
        fontSize = Math.min(parseInt(fontSizeInput.prop("max")), fontSize);
      }
      fontSizeInput.val(fontSize);
      css(activeCell, "fontSize", fontSize);
    }
  });

  $(".font-size-decrease-button", propertiesMenu).on("click", function () {
    if (activeCell) {
      const computedStyle = getComputedStyle(activeCell);
      const fontSizeInput = $(".font-size-input", propertiesMenu);
      let fontSize = fontSizeInput.val()
        ? parseInt(fontSizeInput.val()) - 1
        : parseInt(computedStyle.fontSize);
      if (fontSizeInput.prop("min")) {
        fontSize = Math.max(parseInt(fontSizeInput.prop("min")), fontSize);
      }
      fontSizeInput.val(fontSize);
      css(activeCell, "fontSize", fontSize);
    }
  });

  $(".vertical-align-radio", propertiesMenu).on("change", function () {
    if (activeCell) {
      css(activeCell, "verticalAlign", $(this).val());
    }
  });

  let backgroundColor = "white";
  $(".background-color .cell-color-picker", propertiesMenu)
    .on("click", function () {
      if (activeCell) {
        backgroundColor = getComputedStyle(this).backgroundColor;
        css(activeCell, "backgroundColor", backgroundColor);
        const dropdown = new bootstrap.Dropdown(
          $(".background-color-dropdown", propertiesMenu)[0]
        );
        dropdown.hide();
      }
    })
    .mouseenter(function () {
      if (activeCell) {
        $(activeCell).css(
          "background-color",
          getComputedStyle(this).backgroundColor
        );
      }
    })
    .mouseleave(function () {
      if (activeCell) {
        $(activeCell).css(
          "background-color",
          $(activeCell).data("properties").style.backgroundColor || ""
        );
      }
    });

  $(".bold-toggle-button", propertiesMenu).on("click", function () {
    if (activeCell) {
      if ($(this).hasClass("active")) {
        css(activeCell, "fontWeight", "bold");
      } else {
        css(activeCell, "fontWeight", "");
      }
    }
  });

  $(".text-align-radio", propertiesMenu).on("change", function () {
    if (activeCell) {
      css(activeCell, "textAlign", $(this).val());
    }
  });

  $(".italic-toggle-button", propertiesMenu).on("click", function () {
    if (activeCell) {
      if ($(this).hasClass("active")) {
        css(activeCell, "fontStyle", "italic");
      } else {
        css(activeCell, "fontStyle", "");
      }
    }
  });

  $(".text-color-auto-btn", propertiesMenu).on("click", function () {
    if (activeCell) {
      css(activeCell, "color", textColor);
      const dropdown = new bootstrap.Dropdown(
        $(".text-color-dropdown", propertiesMenu)[0]
      );
      dropdown.hide();
    }
  });

  $(".background-color-auto-btn", propertiesMenu).on("click", function () {
    if (activeCell) {
      css(activeCell, "backgroundColor", backgroundColor);
      const dropdown = new bootstrap.Dropdown(
        $(".background-color-dropdown", propertiesMenu)[0]
      );
      dropdown.hide();
    }
  });

  $(".underline-toggle-button", propertiesMenu).on("click", function () {
    if (activeCell) {
      const properties = $(activeCell).data("properties");
      const textDecoration = properties.style.textDecoration || "";
      const parts = new Set(textDecoration.split(" "));
      if ($(this).hasClass("active")) {
        parts.add("underline");
      } else {
        parts.delete("underline");
      }
      css(activeCell, "textDecoration", Array.from(parts).join(" "));
    }
  });

  $(".strikethrough-toggle-button", propertiesMenu).on("click", function () {
    if (activeCell) {
      const properties = $(activeCell).data("properties");
      const textDecoration = properties.style.textDecoration || "";
      const parts = new Set(textDecoration.split(" "));
      if ($(this).hasClass("active")) {
        parts.add("line-through");
      } else {
        parts.delete("line-through");
      }
      css(activeCell, "textDecoration", Array.from(parts).join(" "));
    }
  });

  const contextMenu = $(`
    <ul class="dropdown-menu show">
      <li><button class="dropdown-item btn btn-sm" href="#"><div class="row"><div class="col-1"><i class="fa-solid fa-copy"></i></div><div class="col-10">Копировать</div></button></li>
      <li><button class="dropdown-item btn btn-sm" href="#"><div class="row"><div class="col-1"><i class="fa-solid fa-paste"></i></div><div class="col-10">Вставить</div></button></li>
      <li><button class="dropdown-item btn btn-sm" href="#"><div class="row"><div class="col-1"></div><div class="col-10">Удалить</div></button></li>
      <li><button class="add-note-button dropdown-item btn btn-sm" href="#"><div class="row"><div class="col-1"><i class="fa-solid fa-note-sticky"></i></div><div class="col-10">Добавить примечание</div></button></li>
      <li><button class="update-note-button dropdown-item btn btn-sm" href="#"><div class="row"><div class="col-1"><i class="fa-solid fa-pen-to-square"></i></div><div class="col-10">Изменить примечание</div></button></li>
      <li><button class="delete-note-button dropdown-item btn btn-sm" href="#"><div class="row"><div class="col-1"><i class="fa-solid fa-eraser"></i></div><div class="col-10">Удалить примечание</div></button></li>
    </ul>
  `).appendTo(document.body);
  hideContextMenu();

  const noteMenu = $(`
		<div class="note-menu card shadow ms-1 mt-1">
			<div class="card-body">
				<div class="form-floating mb-2">
					<textarea class="form-control form-control-sm note-textarea" id="floatingTextarea" style="height: 8em"></textarea>
					<label for="floatingTextarea">Примечание</label>
				</div>
			
				<button class="cancel-button btn btn-sm btn-outline-danger me-2">Отмена</button>
				<button class="submit-button btn btn-sm btn-primary disabled">Подтвердить</button>
			</div>
		</div>
	`);

  $(document).on("click contextmenu", async function () {
    hideNoteMenu();
  });

  noteMenu.on("click contextmenu", function (event) {
    event.stopPropagation();
  });

  function showNoteMenuRelative(cell) {
    $(noteMenu).data("cell", cell);
    noteMenu.appendTo($(cell).offsetParent());
    noteMenu.addClass("active");
    const position = $(cell).offset();
    position.left += $(cell).outerWidth();
    noteMenu.css(position);
    const properties = $(cell).data("properties");
    $(".note-textarea", noteMenu).val(properties && properties.note);
  }

  function hideNoteMenu() {
    noteMenu.removeClass("active");
    $(noteMenu).data("cell", null);
  }

  function checkNoteMenuSubmitRequired() {
    const cell = $(noteMenu).data("cell");
    const properties = $(cell).data("properties");
    const value = $(".note-textarea", noteMenu).val();
    $(".submit-button", noteMenu).toggleClass(
      "disabled",
      !value || value === properties.note
    );
  }

  $(".note-textarea", noteMenu).on("input", checkNoteMenuSubmitRequired);

  $(".cancel-button", noteMenu).on("click", function () {
    hideNoteMenu();
  });

  $(".submit-button", noteMenu).on("click", async function () {
    const cell = $(noteMenu).data("cell");
    const properties = $(cell).data("properties");
    properties.note = $(".note-textarea", noteMenu).val();
    $(cell).addClass("has-note");
    $(cell).data("properties", properties);
    await _saveCell(cell);
    hideNoteMenu();
  });

  $(".add-note-button, .update-note-button", contextMenu).on(
    "click",
    async function () {
      await onCellFocusOut(activeCell);
      showNoteMenuRelative(activeCell);
      checkNoteMenuSubmitRequired();
      $(".note-textarea", noteMenu).focus();
    }
  );

  $(".delete-note-button", contextMenu).on("click", async function () {
    $(activeCell).removeClass("has-note");
    const properties = $(activeCell).data("properties");
    properties.note = null;
    $(activeCell).data("properties", properties);
    await onCellFocusOut(activeCell);
  });

  getRows().then((rows) => {
    if (rows) {
      for (const [row, cells] of rows) {
        insertRow(row, cells);
        for (const [column, cell] of Object.entries(cells)) {
          try {
            const value = cell.value;
            const type = cell.type;
            let properties = cell.properties;
            const readonly = cell.readonly;
            const tr = $(`tr[data-row="${row}"]`, table);
            const cellElement = $(
              `.excel-cell[data-column="${column}"][data-type="${type}"]${
                readonly ? `[data-readonly="true"]` : ""
              }`,
              tr
            );
            cellElement.data("value", value);
            cellElement.data("readonly", readonly);
            if (properties && !properties.style) {
              properties.style = {};
            }
            cellElement.data("properties", properties);
            if (properties) {
              if (properties.style) {
                cellElement.css(properties.style);
              }
              if (properties.note) {
                cellElement.addClass("has-note");
                $(".note .note-content", cellElement).text(properties.note);
              }
            }

            cellElement.html(valueDisplay(cellElement));
            onDisplayStyles(cellElement);
            initializedCells.add(cellElement[0]);
          } catch (error) {
            console.error(error);
          }
        }
      }
    }
    $(table).trigger("cells-loaded");
  });
};
