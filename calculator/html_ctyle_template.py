html_start = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    
<style>

.fa, .fab, .fad, .fal, .far, .fas { -webkit-font-smoothing: antialiased; display: inline-block; font-style: normal; font-variant: normal; text-rendering: auto; line-height: 1; }
.fa-lg { font-size: 1.33333em; line-height: 0.75em; vertical-align: -0.0667em; }
.fa-xs { font-size: 0.75em; }
.fa-sm { font-size: 0.875em; }
.fa-1x { font-size: 1em; }
.fa-2x { font-size: 2em; }
.fa-3x { font-size: 3em; }
.fa-4x { font-size: 4em; }
.fa-5x { font-size: 5em; }
.fa-6x { font-size: 6em; }
.fa-7x { font-size: 7em; }
.fa-8x { font-size: 8em; }
.fa-9x { font-size: 9em; }
.fa-10x { font-size: 10em; }
.fa-fw { text-align: center; width: 1.25em; }
.fa-ul { list-style-type: none; margin-left: 2.5em; padding-left: 0px; }
.fa-ul > li { position: relative; }
.fa-li { left: -2em; position: absolute; text-align: center; width: 2em; line-height: inherit; }
.fa-border { border: 0.08em solid rgb(238, 238, 238); border-radius: 0.1em; padding: 0.2em 0.25em 0.15em; }
.fa-pull-left { float: left; }
.fa-pull-right { float: right; }
.fa.fa-pull-left, .fab.fa-pull-left, .fal.fa-pull-left, .far.fa-pull-left, .fas.fa-pull-left { margin-right: 0.3em; }
.fa.fa-pull-right, .fab.fa-pull-right, .fal.fa-pull-right, .far.fa-pull-right, .fas.fa-pull-right { margin-left: 0.3em; }
.fa-spin { animation: 2s linear 0s infinite normal none running fa-spin; }
.fa-pulse { animation: 1s steps(8) 0s infinite normal none running fa-spin; }
@-webkit-keyframes fa-spin { 
  0% { transform: rotate(0deg); }
  100% { transform: rotate(1turn); }
}
@keyframes fa-spin { 
  0% { transform: rotate(0deg); }
  100% { transform: rotate(1turn); }
}
.fa-rotate-90 { transform: rotate(90deg); }
.fa-rotate-180 { transform: rotate(180deg); }
.fa-rotate-270 { transform: rotate(270deg); }
.fa-flip-horizontal { transform: scaleX(-1); }
.fa-flip-vertical { transform: scaleY(-1); }
.fa-flip-both, .fa-flip-horizontal.fa-flip-vertical, .fa-flip-vertical { }
.fa-flip-both, .fa-flip-horizontal.fa-flip-vertical { transform: scale(-1); }
:root .fa-flip-both, :root .fa-flip-horizontal, :root .fa-flip-vertical, :root .fa-rotate-90, :root .fa-rotate-180, :root .fa-rotate-270 { filter: none; }
.fa-stack { display: inline-block; height: 2em; line-height: 2em; position: relative; vertical-align: middle; width: 2.5em; }
.fa-stack-1x, .fa-stack-2x { left: 0px; position: absolute; text-align: center; width: 100%; }
.fa-stack-1x { line-height: inherit; }
.fa-stack-2x { font-size: 2em; }
.fa-inverse { color: rgb(255, 255, 255); }
.fa-500px::before { content: ""; }
.fa-accessible-icon::before { content: ""; }
.fa-accusoft::before { content: ""; }
.fa-acquisitions-incorporated::before { content: ""; }
.fa-ad::before { content: ""; }
.fa-address-book::before { content: ""; }
.fa-address-card::before { content: ""; }
.fa-adjust::before { content: ""; }
.fa-adn::before { content: ""; }
.fa-adversal::before { content: ""; }
.fa-affiliatetheme::before { content: ""; }
.fa-air-freshener::before { content: ""; }
.fa-airbnb::before { content: ""; }
.fa-algolia::before { content: ""; }
.fa-align-center::before { content: ""; }
.fa-align-justify::before { content: ""; }
.fa-align-left::before { content: ""; }
.fa-align-right::before { content: ""; }
.fa-alipay::before { content: ""; }
.fa-allergies::before { content: ""; }
.fa-amazon::before { content: ""; }
.fa-amazon-pay::before { content: ""; }
.fa-ambulance::before { content: ""; }
.fa-american-sign-language-interpreting::before { content: ""; }
.fa-amilia::before { content: ""; }
.fa-anchor::before { content: ""; }
.fa-android::before { content: ""; }
.fa-angellist::before { content: ""; }
.fa-angle-double-down::before { content: ""; }
.fa-angle-double-left::before { content: ""; }
.fa-angle-double-right::before { content: ""; }
.fa-angle-double-up::before { content: ""; }
.fa-angle-down::before { content: ""; }
.fa-angle-left::before { content: ""; }
.fa-angle-right::before { content: ""; }
.fa-angle-up::before { content: ""; }
.fa-angry::before { content: ""; }
.fa-angrycreative::before { content: ""; }
.fa-angular::before { content: ""; }
.fa-ankh::before { content: ""; }
.fa-app-store::before { content: ""; }
.fa-app-store-ios::before { content: ""; }
.fa-apper::before { content: ""; }
.fa-apple::before { content: ""; }
.fa-apple-alt::before { content: ""; }
.fa-apple-pay::before { content: ""; }
.fa-archive::before { content: ""; }
.fa-archway::before { content: ""; }
.fa-arrow-alt-circle-down::before { content: ""; }
.fa-arrow-alt-circle-left::before { content: ""; }
.fa-arrow-alt-circle-right::before { content: ""; }
.fa-arrow-alt-circle-up::before { content: ""; }
.fa-arrow-circle-down::before { content: ""; }
.fa-arrow-circle-left::before { content: ""; }
.fa-arrow-circle-right::before { content: ""; }
.fa-arrow-circle-up::before { content: ""; }
.fa-arrow-down::before { content: ""; }
.fa-arrow-left::before { content: ""; }
.fa-arrow-right::before { content: ""; }
.fa-arrow-up::before { content: ""; }
.fa-arrows-alt::before { content: ""; }
.fa-arrows-alt-h::before { content: ""; }
.fa-arrows-alt-v::before { content: ""; }
.fa-artstation::before { content: ""; }
.fa-assistive-listening-systems::before { content: ""; }
.fa-asterisk::before { content: ""; }
.fa-asymmetrik::before { content: ""; }
.fa-at::before { content: ""; }
.fa-atlas::before { content: ""; }
.fa-atlassian::before { content: ""; }
.fa-atom::before { content: ""; }
.fa-audible::before { content: ""; }
.fa-audio-description::before { content: ""; }
.fa-autoprefixer::before { content: ""; }
.fa-avianex::before { content: ""; }
.fa-aviato::before { content: ""; }
.fa-award::before { content: ""; }
.fa-aws::before { content: ""; }
.fa-baby::before { content: ""; }
.fa-baby-carriage::before { content: ""; }
.fa-backspace::before { content: ""; }
.fa-backward::before { content: ""; }
.fa-bacon::before { content: ""; }
.fa-bacteria::before { content: ""; }
.fa-bacterium::before { content: ""; }
.fa-bahai::before { content: ""; }
.fa-balance-scale::before { content: ""; }
.fa-balance-scale-left::before { content: ""; }
.fa-balance-scale-right::before { content: ""; }
.fa-ban::before { content: ""; }
.fa-band-aid::before { content: ""; }
.fa-bandcamp::before { content: ""; }
.fa-barcode::before { content: ""; }
.fa-bars::before { content: ""; }
.fa-baseball-ball::before { content: ""; }
.fa-basketball-ball::before { content: ""; }
.fa-bath::before { content: ""; }
.fa-battery-empty::before { content: ""; }
.fa-battery-full::before { content: ""; }
.fa-battery-half::before { content: ""; }
.fa-battery-quarter::before { content: ""; }
.fa-battery-three-quarters::before { content: ""; }
.fa-battle-net::before { content: ""; }
.fa-bed::before { content: ""; }
.fa-beer::before { content: ""; }
.fa-behance::before { content: ""; }
.fa-behance-square::before { content: ""; }
.fa-bell::before { content: ""; }
.fa-bell-slash::before { content: ""; }
.fa-bezier-curve::before { content: ""; }
.fa-bible::before { content: ""; }
.fa-bicycle::before { content: ""; }
.fa-biking::before { content: ""; }
.fa-bimobject::before { content: ""; }
.fa-binoculars::before { content: ""; }
.fa-biohazard::before { content: ""; }
.fa-birthday-cake::before { content: ""; }
.fa-bitbucket::before { content: ""; }
.fa-bitcoin::before { content: ""; }
.fa-bity::before { content: ""; }
.fa-black-tie::before { content: ""; }
.fa-blackberry::before { content: ""; }
.fa-blender::before { content: ""; }
.fa-blender-phone::before { content: ""; }
.fa-blind::before { content: ""; }
.fa-blog::before { content: ""; }
.fa-blogger::before { content: ""; }
.fa-blogger-b::before { content: ""; }
.fa-bluetooth::before { content: ""; }
.fa-bluetooth-b::before { content: ""; }
.fa-bold::before { content: ""; }
.fa-bolt::before { content: ""; }
.fa-bomb::before { content: ""; }
.fa-bone::before { content: ""; }
.fa-bong::before { content: ""; }
.fa-book::before { content: ""; }
.fa-book-dead::before { content: ""; }
.fa-book-medical::before { content: ""; }
.fa-book-open::before { content: ""; }
.fa-book-reader::before { content: ""; }
.fa-bookmark::before { content: ""; }
.fa-bootstrap::before { content: ""; }
.fa-border-all::before { content: ""; }
.fa-border-none::before { content: ""; }
.fa-border-style::before { content: ""; }
.fa-bowling-ball::before { content: ""; }
.fa-box::before { content: ""; }
.fa-box-open::before { content: ""; }
.fa-box-tissue::before { content: ""; }
.fa-boxes::before { content: ""; }
.fa-braille::before { content: ""; }
.fa-brain::before { content: ""; }
.fa-bread-slice::before { content: ""; }
.fa-briefcase::before { content: ""; }
.fa-briefcase-medical::before { content: ""; }
.fa-broadcast-tower::before { content: ""; }
.fa-broom::before { content: ""; }
.fa-brush::before { content: ""; }
.fa-btc::before { content: ""; }
.fa-buffer::before { content: ""; }
.fa-bug::before { content: ""; }
.fa-building::before { content: ""; }
.fa-bullhorn::before { content: ""; }
.fa-bullseye::before { content: ""; }
.fa-burn::before { content: ""; }
.fa-buromobelexperte::before { content: ""; }
.fa-bus::before { content: ""; }
.fa-bus-alt::before { content: ""; }
.fa-business-time::before { content: ""; }
.fa-buy-n-large::before { content: ""; }
.fa-buysellads::before { content: ""; }
.fa-calculator::before { content: ""; }
.fa-calendar::before { content: ""; }
.fa-calendar-alt::before { content: ""; }
.fa-calendar-check::before { content: ""; }
.fa-calendar-day::before { content: ""; }
.fa-calendar-minus::before { content: ""; }
.fa-calendar-plus::before { content: ""; }
.fa-calendar-times::before { content: ""; }
.fa-calendar-week::before { content: ""; }
.fa-camera::before { content: ""; }
.fa-camera-retro::before { content: ""; }
.fa-campground::before { content: ""; }
.fa-canadian-maple-leaf::before { content: ""; }
.fa-candy-cane::before { content: ""; }
.fa-cannabis::before { content: ""; }
.fa-capsules::before { content: ""; }
.fa-car::before { content: ""; }
.fa-car-alt::before { content: ""; }
.fa-car-battery::before { content: ""; }
.fa-car-crash::before { content: ""; }
.fa-car-side::before { content: ""; }
.fa-caravan::before { content: ""; }
.fa-caret-down::before { content: ""; }
.fa-caret-left::before { content: ""; }
.fa-caret-right::before { content: ""; }
.fa-caret-square-down::before { content: ""; }
.fa-caret-square-left::before { content: ""; }
.fa-caret-square-right::before { content: ""; }
.fa-caret-square-up::before { content: ""; }
.fa-caret-up::before { content: ""; }
.fa-carrot::before { content: ""; }
.fa-cart-arrow-down::before { content: ""; }
.fa-cart-plus::before { content: ""; }
.fa-cash-register::before { content: ""; }
.fa-cat::before { content: ""; }
.fa-cc-amazon-pay::before { content: ""; }
.fa-cc-amex::before { content: ""; }
.fa-cc-apple-pay::before { content: ""; }
.fa-cc-diners-club::before { content: ""; }
.fa-cc-discover::before { content: ""; }
.fa-cc-jcb::before { content: ""; }
.fa-cc-mastercard::before { content: ""; }
.fa-cc-paypal::before { content: ""; }
.fa-cc-stripe::before { content: ""; }
.fa-cc-visa::before { content: ""; }
.fa-centercode::before { content: ""; }
.fa-centos::before { content: ""; }
.fa-certificate::before { content: ""; }
.fa-chair::before { content: ""; }
.fa-chalkboard::before { content: ""; }
.fa-chalkboard-teacher::before { content: ""; }
.fa-charging-station::before { content: ""; }
.fa-chart-area::before { content: ""; }
.fa-chart-bar::before { content: ""; }
.fa-chart-line::before { content: ""; }
.fa-chart-pie::before { content: ""; }
.fa-check::before { content: ""; }
.fa-check-circle::before { content: ""; }
.fa-check-double::before { content: ""; }
.fa-check-square::before { content: ""; }
.fa-cheese::before { content: ""; }
.fa-chess::before { content: ""; }
.fa-chess-bishop::before { content: ""; }
.fa-chess-board::before { content: ""; }
.fa-chess-king::before { content: ""; }
.fa-chess-knight::before { content: ""; }
.fa-chess-pawn::before { content: ""; }
.fa-chess-queen::before { content: ""; }
.fa-chess-rook::before { content: ""; }
.fa-chevron-circle-down::before { content: ""; }
.fa-chevron-circle-left::before { content: ""; }
.fa-chevron-circle-right::before { content: ""; }
.fa-chevron-circle-up::before { content: ""; }
.fa-chevron-down::before { content: ""; }
.fa-chevron-left::before { content: ""; }
.fa-chevron-right::before { content: ""; }
.fa-chevron-up::before { content: ""; }
.fa-child::before { content: ""; }
.fa-chrome::before { content: ""; }
.fa-chromecast::before { content: ""; }
.fa-church::before { content: ""; }
.fa-circle::before { content: ""; }
.fa-circle-notch::before { content: ""; }
.fa-city::before { content: ""; }
.fa-clinic-medical::before { content: ""; }
.fa-clipboard::before { content: ""; }
.fa-clipboard-check::before { content: ""; }
.fa-clipboard-list::before { content: ""; }
.fa-clock::before { content: ""; }
.fa-clone::before { content: ""; }
.fa-closed-captioning::before { content: ""; }
.fa-cloud::before { content: ""; }
.fa-cloud-download-alt::before { content: ""; }
.fa-cloud-meatball::before { content: ""; }
.fa-cloud-moon::before { content: ""; }
.fa-cloud-moon-rain::before { content: ""; }
.fa-cloud-rain::before { content: ""; }
.fa-cloud-showers-heavy::before { content: ""; }
.fa-cloud-sun::before { content: ""; }
.fa-cloud-sun-rain::before { content: ""; }
.fa-cloud-upload-alt::before { content: ""; }
.fa-cloudflare::before { content: ""; }
.fa-cloudscale::before { content: ""; }
.fa-cloudsmith::before { content: ""; }
.fa-cloudversify::before { content: ""; }
.fa-cocktail::before { content: ""; }
.fa-code::before { content: ""; }
.fa-code-branch::before { content: ""; }
.fa-codepen::before { content: ""; }
.fa-codiepie::before { content: ""; }
.fa-coffee::before { content: ""; }
.fa-cog::before { content: ""; }
.fa-cogs::before { content: ""; }
.fa-coins::before { content: ""; }
.fa-columns::before { content: ""; }
.fa-comment::before { content: ""; }
.fa-comment-alt::before { content: ""; }
.fa-comment-dollar::before { content: ""; }
.fa-comment-dots::before { content: ""; }
.fa-comment-medical::before { content: ""; }
.fa-comment-slash::before { content: ""; }
.fa-comments::before { content: ""; }
.fa-comments-dollar::before { content: ""; }
.fa-compact-disc::before { content: ""; }
.fa-compass::before { content: ""; }
.fa-compress::before { content: ""; }
.fa-compress-alt::before { content: ""; }
.fa-compress-arrows-alt::before { content: ""; }
.fa-concierge-bell::before { content: ""; }
.fa-confluence::before { content: ""; }
.fa-connectdevelop::before { content: ""; }
.fa-contao::before { content: ""; }
.fa-cookie::before { content: ""; }
.fa-cookie-bite::before { content: ""; }
.fa-copy::before { content: ""; }
.fa-copyright::before { content: ""; }
.fa-cotton-bureau::before { content: ""; }
.fa-couch::before { content: ""; }
.fa-cpanel::before { content: ""; }
.fa-creative-commons::before { content: ""; }
.fa-creative-commons-by::before { content: ""; }
.fa-creative-commons-nc::before { content: ""; }
.fa-creative-commons-nc-eu::before { content: ""; }
.fa-creative-commons-nc-jp::before { content: ""; }
.fa-creative-commons-nd::before { content: ""; }
.fa-creative-commons-pd::before { content: ""; }
.fa-creative-commons-pd-alt::before { content: ""; }
.fa-creative-commons-remix::before { content: ""; }
.fa-creative-commons-sa::before { content: ""; }
.fa-creative-commons-sampling::before { content: ""; }
.fa-creative-commons-sampling-plus::before { content: ""; }
.fa-creative-commons-share::before { content: ""; }
.fa-creative-commons-zero::before { content: ""; }
.fa-credit-card::before { content: ""; }
.fa-critical-role::before { content: ""; }
.fa-crop::before { content: ""; }
.fa-crop-alt::before { content: ""; }
.fa-cross::before { content: ""; }
.fa-crosshairs::before { content: ""; }
.fa-crow::before { content: ""; }
.fa-crown::before { content: ""; }
.fa-crutch::before { content: ""; }
.fa-css3::before { content: ""; }
.fa-css3-alt::before { content: ""; }
.fa-cube::before { content: ""; }
.fa-cubes::before { content: ""; }
.fa-cut::before { content: ""; }
.fa-cuttlefish::before { content: ""; }
.fa-d-and-d::before { content: ""; }
.fa-d-and-d-beyond::before { content: ""; }
.fa-dailymotion::before { content: ""; }
.fa-dashcube::before { content: ""; }
.fa-database::before { content: ""; }
.fa-deaf::before { content: ""; }
.fa-deezer::before { content: ""; }
.fa-delicious::before { content: ""; }
.fa-democrat::before { content: ""; }
.fa-deploydog::before { content: ""; }
.fa-deskpro::before { content: ""; }
.fa-desktop::before { content: ""; }
.fa-dev::before { content: ""; }
.fa-deviantart::before { content: ""; }
.fa-dharmachakra::before { content: ""; }
.fa-dhl::before { content: ""; }
.fa-diagnoses::before { content: ""; }
.fa-diaspora::before { content: ""; }
.fa-dice::before { content: ""; }
.fa-dice-d20::before { content: ""; }
.fa-dice-d6::before { content: ""; }
.fa-dice-five::before { content: ""; }
.fa-dice-four::before { content: ""; }
.fa-dice-one::before { content: ""; }
.fa-dice-six::before { content: ""; }
.fa-dice-three::before { content: ""; }
.fa-dice-two::before { content: ""; }
.fa-digg::before { content: ""; }
.fa-digital-ocean::before { content: ""; }
.fa-digital-tachograph::before { content: ""; }
.fa-directions::before { content: ""; }
.fa-discord::before { content: ""; }
.fa-discourse::before { content: ""; }
.fa-disease::before { content: ""; }
.fa-divide::before { content: ""; }
.fa-dizzy::before { content: ""; }
.fa-dna::before { content: ""; }
.fa-dochub::before { content: ""; }
.fa-docker::before { content: ""; }
.fa-dog::before { content: ""; }
.fa-dollar-sign::before { content: ""; }
.fa-dolly::before { content: ""; }
.fa-dolly-flatbed::before { content: ""; }
.fa-donate::before { content: ""; }
.fa-door-closed::before { content: ""; }
.fa-door-open::before { content: ""; }
.fa-dot-circle::before { content: ""; }
.fa-dove::before { content: ""; }
.fa-download::before { content: ""; }
.fa-draft2digital::before { content: ""; }
.fa-drafting-compass::before { content: ""; }
.fa-dragon::before { content: ""; }
.fa-draw-polygon::before { content: ""; }
.fa-dribbble::before { content: ""; }
.fa-dribbble-square::before { content: ""; }
.fa-dropbox::before { content: ""; }
.fa-drum::before { content: ""; }
.fa-drum-steelpan::before { content: ""; }
.fa-drumstick-bite::before { content: ""; }
.fa-drupal::before { content: ""; }
.fa-dumbbell::before { content: ""; }
.fa-dumpster::before { content: ""; }
.fa-dumpster-fire::before { content: ""; }
.fa-dungeon::before { content: ""; }
.fa-dyalog::before { content: ""; }
.fa-earlybirds::before { content: ""; }
.fa-ebay::before { content: ""; }
.fa-edge::before { content: ""; }
.fa-edge-legacy::before { content: ""; }
.fa-edit::before { content: ""; }
.fa-egg::before { content: ""; }
.fa-eject::before { content: ""; }
.fa-elementor::before { content: ""; }
.fa-ellipsis-h::before { content: ""; }
.fa-ellipsis-v::before { content: ""; }
.fa-ello::before { content: ""; }
.fa-ember::before { content: ""; }
.fa-empire::before { content: ""; }
.fa-envelope::before { content: ""; }
.fa-envelope-open::before { content: ""; }
.fa-envelope-open-text::before { content: ""; }
.fa-envelope-square::before { content: ""; }
.fa-envira::before { content: ""; }
.fa-equals::before { content: ""; }
.fa-eraser::before { content: ""; }
.fa-erlang::before { content: ""; }
.fa-ethereum::before { content: ""; }
.fa-ethernet::before { content: ""; }
.fa-etsy::before { content: ""; }
.fa-euro-sign::before { content: ""; }
.fa-evernote::before { content: ""; }
.fa-exchange-alt::before { content: ""; }
.fa-exclamation::before { content: ""; }
.fa-exclamation-circle::before { content: ""; }
.fa-exclamation-triangle::before { content: ""; }
.fa-expand::before { content: ""; }
.fa-expand-alt::before { content: ""; }
.fa-expand-arrows-alt::before { content: ""; }
.fa-expeditedssl::before { content: ""; }
.fa-external-link-alt::before { content: ""; }
.fa-external-link-square-alt::before { content: ""; }
.fa-eye::before { content: ""; }
.fa-eye-dropper::before { content: ""; }
.fa-eye-slash::before { content: ""; }
.fa-facebook::before { content: ""; }
.fa-facebook-f::before { content: ""; }
.fa-facebook-messenger::before { content: ""; }
.fa-facebook-square::before { content: ""; }
.fa-fan::before { content: ""; }
.fa-fantasy-flight-games::before { content: ""; }
.fa-fast-backward::before { content: ""; }
.fa-fast-forward::before { content: ""; }
.fa-faucet::before { content: ""; }
.fa-fax::before { content: ""; }
.fa-feather::before { content: ""; }
.fa-feather-alt::before { content: ""; }
.fa-fedex::before { content: ""; }
.fa-fedora::before { content: ""; }
.fa-female::before { content: ""; }
.fa-fighter-jet::before { content: ""; }
.fa-figma::before { content: ""; }
.fa-file::before { content: ""; }
.fa-file-alt::before { content: ""; }
.fa-file-archive::before { content: ""; }
.fa-file-audio::before { content: ""; }
.fa-file-code::before { content: ""; }
.fa-file-contract::before { content: ""; }
.fa-file-csv::before { content: ""; }
.fa-file-download::before { content: ""; }
.fa-file-excel::before { content: ""; }
.fa-file-export::before { content: ""; }
.fa-file-image::before { content: ""; }
.fa-file-import::before { content: ""; }
.fa-file-invoice::before { content: ""; }
.fa-file-invoice-dollar::before { content: ""; }
.fa-file-medical::before { content: ""; }
.fa-file-medical-alt::before { content: ""; }
.fa-file-pdf::before { content: ""; }
.fa-file-powerpoint::before { content: ""; }
.fa-file-prescription::before { content: ""; }
.fa-file-signature::before { content: ""; }
.fa-file-upload::before { content: ""; }
.fa-file-video::before { content: ""; }
.fa-file-word::before { content: ""; }
.fa-fill::before { content: ""; }
.fa-fill-drip::before { content: ""; }
.fa-film::before { content: ""; }
.fa-filter::before { content: ""; }
.fa-fingerprint::before { content: ""; }
.fa-fire::before { content: ""; }
.fa-fire-alt::before { content: ""; }
.fa-fire-extinguisher::before { content: ""; }
.fa-firefox::before { content: ""; }
.fa-firefox-browser::before { content: ""; }
.fa-first-aid::before { content: ""; }
.fa-first-order::before { content: ""; }
.fa-first-order-alt::before { content: ""; }
.fa-firstdraft::before { content: ""; }
.fa-fish::before { content: ""; }
.fa-fist-raised::before { content: ""; }
.fa-flag::before { content: ""; }
.fa-flag-checkered::before { content: ""; }
.fa-flag-usa::before { content: ""; }
.fa-flask::before { content: ""; }
.fa-flickr::before { content: ""; }
.fa-flipboard::before { content: ""; }
.fa-flushed::before { content: ""; }
.fa-fly::before { content: ""; }
.fa-folder::before { content: ""; }
.fa-folder-minus::before { content: ""; }
.fa-folder-open::before { content: ""; }
.fa-folder-plus::before { content: ""; }
.fa-font::before { content: ""; }
.fa-font-awesome::before { content: ""; }
.fa-font-awesome-alt::before { content: ""; }
.fa-font-awesome-flag::before { content: ""; }
.fa-font-awesome-logo-full::before { content: ""; }
.fa-fonticons::before { content: ""; }
.fa-fonticons-fi::before { content: ""; }
.fa-football-ball::before { content: ""; }
.fa-fort-awesome::before { content: ""; }
.fa-fort-awesome-alt::before { content: ""; }
.fa-forumbee::before { content: ""; }
.fa-forward::before { content: ""; }
.fa-foursquare::before { content: ""; }
.fa-free-code-camp::before { content: ""; }
.fa-freebsd::before { content: ""; }
.fa-frog::before { content: ""; }
.fa-frown::before { content: ""; }
.fa-frown-open::before { content: ""; }
.fa-fulcrum::before { content: ""; }
.fa-funnel-dollar::before { content: ""; }
.fa-futbol::before { content: ""; }
.fa-galactic-republic::before { content: ""; }
.fa-galactic-senate::before { content: ""; }
.fa-gamepad::before { content: ""; }
.fa-gas-pump::before { content: ""; }
.fa-gavel::before { content: ""; }
.fa-gem::before { content: ""; }
.fa-genderless::before { content: ""; }
.fa-get-pocket::before { content: ""; }
.fa-gg::before { content: ""; }
.fa-gg-circle::before { content: ""; }
.fa-ghost::before { content: ""; }
.fa-gift::before { content: ""; }
.fa-gifts::before { content: ""; }
.fa-git::before { content: ""; }
.fa-git-alt::before { content: ""; }
.fa-git-square::before { content: ""; }
.fa-github::before { content: ""; }
.fa-github-alt::before { content: ""; }
.fa-github-square::before { content: ""; }
.fa-gitkraken::before { content: ""; }
.fa-gitlab::before { content: ""; }
.fa-gitter::before { content: ""; }
.fa-glass-cheers::before { content: ""; }
.fa-glass-martini::before { content: ""; }
.fa-glass-martini-alt::before { content: ""; }
.fa-glass-whiskey::before { content: ""; }
.fa-glasses::before { content: ""; }
.fa-glide::before { content: ""; }
.fa-glide-g::before { content: ""; }
.fa-globe::before { content: ""; }
.fa-globe-africa::before { content: ""; }
.fa-globe-americas::before { content: ""; }
.fa-globe-asia::before { content: ""; }
.fa-globe-europe::before { content: ""; }
.fa-gofore::before { content: ""; }
.fa-golf-ball::before { content: ""; }
.fa-goodreads::before { content: ""; }
.fa-goodreads-g::before { content: ""; }
.fa-google::before { content: ""; }
.fa-google-drive::before { content: ""; }
.fa-google-pay::before { content: ""; }
.fa-google-play::before { content: ""; }
.fa-google-plus::before { content: ""; }
.fa-google-plus-g::before { content: ""; }
.fa-google-plus-square::before { content: ""; }
.fa-google-wallet::before { content: ""; }
.fa-gopuram::before { content: ""; }
.fa-graduation-cap::before { content: ""; }
.fa-gratipay::before { content: ""; }
.fa-grav::before { content: ""; }
.fa-greater-than::before { content: ""; }
.fa-greater-than-equal::before { content: ""; }
.fa-grimace::before { content: ""; }
.fa-grin::before { content: ""; }
.fa-grin-alt::before { content: ""; }
.fa-grin-beam::before { content: ""; }
.fa-grin-beam-sweat::before { content: ""; }
.fa-grin-hearts::before { content: ""; }
.fa-grin-squint::before { content: ""; }
.fa-grin-squint-tears::before { content: ""; }
.fa-grin-stars::before { content: ""; }
.fa-grin-tears::before { content: ""; }
.fa-grin-tongue::before { content: ""; }
.fa-grin-tongue-squint::before { content: ""; }
.fa-grin-tongue-wink::before { content: ""; }
.fa-grin-wink::before { content: ""; }
.fa-grip-horizontal::before { content: ""; }
.fa-grip-lines::before { content: ""; }
.fa-grip-lines-vertical::before { content: ""; }
.fa-grip-vertical::before { content: ""; }
.fa-gripfire::before { content: ""; }
.fa-grunt::before { content: ""; }
.fa-guilded::before { content: ""; }
.fa-guitar::before { content: ""; }
.fa-gulp::before { content: ""; }
.fa-h-square::before { content: ""; }
.fa-hacker-news::before { content: ""; }
.fa-hacker-news-square::before { content: ""; }
.fa-hackerrank::before { content: ""; }
.fa-hamburger::before { content: ""; }
.fa-hammer::before { content: ""; }
.fa-hamsa::before { content: ""; }
.fa-hand-holding::before { content: ""; }
.fa-hand-holding-heart::before { content: ""; }
.fa-hand-holding-medical::before { content: ""; }
.fa-hand-holding-usd::before { content: ""; }
.fa-hand-holding-water::before { content: ""; }
.fa-hand-lizard::before { content: ""; }
.fa-hand-middle-finger::before { content: ""; }
.fa-hand-paper::before { content: ""; }
.fa-hand-peace::before { content: ""; }
.fa-hand-point-down::before { content: ""; }
.fa-hand-point-left::before { content: ""; }
.fa-hand-point-right::before { content: ""; }
.fa-hand-point-up::before { content: ""; }
.fa-hand-pointer::before { content: ""; }
.fa-hand-rock::before { content: ""; }
.fa-hand-scissors::before { content: ""; }
.fa-hand-sparkles::before { content: ""; }
.fa-hand-spock::before { content: ""; }
.fa-hands::before { content: ""; }
.fa-hands-helping::before { content: ""; }
.fa-hands-wash::before { content: ""; }
.fa-handshake::before { content: ""; }
.fa-handshake-alt-slash::before { content: ""; }
.fa-handshake-slash::before { content: ""; }
.fa-hanukiah::before { content: ""; }
.fa-hard-hat::before { content: ""; }
.fa-hashtag::before { content: ""; }
.fa-hat-cowboy::before { content: ""; }
.fa-hat-cowboy-side::before { content: ""; }
.fa-hat-wizard::before { content: ""; }
.fa-hdd::before { content: ""; }
.fa-head-side-cough::before { content: ""; }
.fa-head-side-cough-slash::before { content: ""; }
.fa-head-side-mask::before { content: ""; }
.fa-head-side-virus::before { content: ""; }
.fa-heading::before { content: ""; }
.fa-headphones::before { content: ""; }
.fa-headphones-alt::before { content: ""; }
.fa-headset::before { content: ""; }
.fa-heart::before { content: ""; }
.fa-heart-broken::before { content: ""; }
.fa-heartbeat::before { content: ""; }
.fa-helicopter::before { content: ""; }
.fa-highlighter::before { content: ""; }
.fa-hiking::before { content: ""; }
.fa-hippo::before { content: ""; }
.fa-hips::before { content: ""; }
.fa-hire-a-helper::before { content: ""; }
.fa-history::before { content: ""; }
.fa-hive::before { content: ""; }
.fa-hockey-puck::before { content: ""; }
.fa-holly-berry::before { content: ""; }
.fa-home::before { content: ""; }
.fa-hooli::before { content: ""; }
.fa-hornbill::before { content: ""; }
.fa-horse::before { content: ""; }
.fa-horse-head::before { content: ""; }
.fa-hospital::before { content: ""; }
.fa-hospital-alt::before { content: ""; }
.fa-hospital-symbol::before { content: ""; }
.fa-hospital-user::before { content: ""; }
.fa-hot-tub::before { content: ""; }
.fa-hotdog::before { content: ""; }
.fa-hotel::before { content: ""; }
.fa-hotjar::before { content: ""; }
.fa-hourglass::before { content: ""; }
.fa-hourglass-end::before { content: ""; }
.fa-hourglass-half::before { content: ""; }
.fa-hourglass-start::before { content: ""; }
.fa-house-damage::before { content: ""; }
.fa-house-user::before { content: ""; }
.fa-houzz::before { content: ""; }
.fa-hryvnia::before { content: ""; }
.fa-html5::before { content: ""; }
.fa-hubspot::before { content: ""; }
.fa-i-cursor::before { content: ""; }
.fa-ice-cream::before { content: ""; }
.fa-icicles::before { content: ""; }
.fa-icons::before { content: ""; }
.fa-id-badge::before { content: ""; }
.fa-id-card::before { content: ""; }
.fa-id-card-alt::before { content: ""; }
.fa-ideal::before { content: ""; }
.fa-igloo::before { content: ""; }
.fa-image::before { content: ""; }
.fa-images::before { content: ""; }
.fa-imdb::before { content: ""; }
.fa-inbox::before { content: ""; }
.fa-indent::before { content: ""; }
.fa-industry::before { content: ""; }
.fa-infinity::before { content: ""; }
.fa-info::before { content: ""; }
.fa-info-circle::before { content: ""; }
.fa-innosoft::before { content: ""; }
.fa-instagram::before { content: ""; }
.fa-instagram-square::before { content: ""; }
.fa-instalod::before { content: ""; }
.fa-intercom::before { content: ""; }
.fa-internet-explorer::before { content: ""; }
.fa-invision::before { content: ""; }
.fa-ioxhost::before { content: ""; }
.fa-italic::before { content: ""; }
.fa-itch-io::before { content: ""; }
.fa-itunes::before { content: ""; }
.fa-itunes-note::before { content: ""; }
.fa-java::before { content: ""; }
.fa-jedi::before { content: ""; }
.fa-jedi-order::before { content: ""; }
.fa-jenkins::before { content: ""; }
.fa-jira::before { content: ""; }
.fa-joget::before { content: ""; }
.fa-joint::before { content: ""; }
.fa-joomla::before { content: ""; }
.fa-journal-whills::before { content: ""; }
.fa-js::before { content: ""; }
.fa-js-square::before { content: ""; }
.fa-jsfiddle::before { content: ""; }
.fa-kaaba::before { content: ""; }
.fa-kaggle::before { content: ""; }
.fa-key::before { content: ""; }
.fa-keybase::before { content: ""; }
.fa-keyboard::before { content: ""; }
.fa-keycdn::before { content: ""; }
.fa-khanda::before { content: ""; }
.fa-kickstarter::before { content: ""; }
.fa-kickstarter-k::before { content: ""; }
.fa-kiss::before { content: ""; }
.fa-kiss-beam::before { content: ""; }
.fa-kiss-wink-heart::before { content: ""; }
.fa-kiwi-bird::before { content: ""; }
.fa-korvue::before { content: ""; }
.fa-landmark::before { content: ""; }
.fa-language::before { content: ""; }
.fa-laptop::before { content: ""; }
.fa-laptop-code::before { content: ""; }
.fa-laptop-house::before { content: ""; }
.fa-laptop-medical::before { content: ""; }
.fa-laravel::before { content: ""; }
.fa-lastfm::before { content: ""; }
.fa-lastfm-square::before { content: ""; }
.fa-laugh::before { content: ""; }
.fa-laugh-beam::before { content: ""; }
.fa-laugh-squint::before { content: ""; }
.fa-laugh-wink::before { content: ""; }
.fa-layer-group::before { content: ""; }
.fa-leaf::before { content: ""; }
.fa-leanpub::before { content: ""; }
.fa-lemon::before { content: ""; }
.fa-less::before { content: ""; }
.fa-less-than::before { content: ""; }
.fa-less-than-equal::before { content: ""; }
.fa-level-down-alt::before { content: ""; }
.fa-level-up-alt::before { content: ""; }
.fa-life-ring::before { content: ""; }
.fa-lightbulb::before { content: ""; }
.fa-line::before { content: ""; }
.fa-link::before { content: ""; }
.fa-linkedin::before { content: ""; }
.fa-linkedin-in::before { content: ""; }
.fa-linode::before { content: ""; }
.fa-linux::before { content: ""; }
.fa-lira-sign::before { content: ""; }
.fa-list::before { content: ""; }
.fa-list-alt::before { content: ""; }
.fa-list-ol::before { content: ""; }
.fa-list-ul::before { content: ""; }
.fa-location-arrow::before { content: ""; }
.fa-lock::before { content: ""; }
.fa-lock-open::before { content: ""; }
.fa-long-arrow-alt-down::before { content: ""; }
.fa-long-arrow-alt-left::before { content: ""; }
.fa-long-arrow-alt-right::before { content: ""; }
.fa-long-arrow-alt-up::before { content: ""; }
.fa-low-vision::before { content: ""; }
.fa-luggage-cart::before { content: ""; }
.fa-lungs::before { content: ""; }
.fa-lungs-virus::before { content: ""; }
.fa-lyft::before { content: ""; }
.fa-magento::before { content: ""; }
.fa-magic::before { content: ""; }
.fa-magnet::before { content: ""; }
.fa-mail-bulk::before { content: ""; }
.fa-mailchimp::before { content: ""; }
.fa-male::before { content: ""; }
.fa-mandalorian::before { content: ""; }
.fa-map::before { content: ""; }
.fa-map-marked::before { content: ""; }
.fa-map-marked-alt::before { content: ""; }
.fa-map-marker::before { content: ""; }
.fa-map-marker-alt::before { content: ""; }
.fa-map-pin::before { content: ""; }
.fa-map-signs::before { content: ""; }
.fa-markdown::before { content: ""; }
.fa-marker::before { content: ""; }
.fa-mars::before { content: ""; }
.fa-mars-double::before { content: ""; }
.fa-mars-stroke::before { content: ""; }
.fa-mars-stroke-h::before { content: ""; }
.fa-mars-stroke-v::before { content: ""; }
.fa-mask::before { content: ""; }
.fa-mastodon::before { content: ""; }
.fa-maxcdn::before { content: ""; }
.fa-mdb::before { content: ""; }
.fa-medal::before { content: ""; }
.fa-medapps::before { content: ""; }
.fa-medium::before { content: ""; }
.fa-medium-m::before { content: ""; }
.fa-medkit::before { content: ""; }
.fa-medrt::before { content: ""; }
.fa-meetup::before { content: ""; }
.fa-megaport::before { content: ""; }
.fa-meh::before { content: ""; }
.fa-meh-blank::before { content: ""; }
.fa-meh-rolling-eyes::before { content: ""; }
.fa-memory::before { content: ""; }
.fa-mendeley::before { content: ""; }
.fa-menorah::before { content: ""; }
.fa-mercury::before { content: ""; }
.fa-meteor::before { content: ""; }
.fa-microblog::before { content: ""; }
.fa-microchip::before { content: ""; }
.fa-microphone::before { content: ""; }
.fa-microphone-alt::before { content: ""; }
.fa-microphone-alt-slash::before { content: ""; }
.fa-microphone-slash::before { content: ""; }
.fa-microscope::before { content: ""; }
.fa-microsoft::before { content: ""; }
.fa-minus::before { content: ""; }
.fa-minus-circle::before { content: ""; }
.fa-minus-square::before { content: ""; }
.fa-mitten::before { content: ""; }
.fa-mix::before { content: ""; }
.fa-mixcloud::before { content: ""; }
.fa-mixer::before { content: ""; }
.fa-mizuni::before { content: ""; }
.fa-mobile::before { content: ""; }
.fa-mobile-alt::before { content: ""; }
.fa-modx::before { content: ""; }
.fa-monero::before { content: ""; }
.fa-money-bill::before { content: ""; }
.fa-money-bill-alt::before { content: ""; }
.fa-money-bill-wave::before { content: ""; }
.fa-money-bill-wave-alt::before { content: ""; }
.fa-money-check::before { content: ""; }
.fa-money-check-alt::before { content: ""; }
.fa-monument::before { content: ""; }
.fa-moon::before { content: ""; }
.fa-mortar-pestle::before { content: ""; }
.fa-mosque::before { content: ""; }
.fa-motorcycle::before { content: ""; }
.fa-mountain::before { content: ""; }
.fa-mouse::before { content: ""; }
.fa-mouse-pointer::before { content: ""; }
.fa-mug-hot::before { content: ""; }
.fa-music::before { content: ""; }
.fa-napster::before { content: ""; }
.fa-neos::before { content: ""; }
.fa-network-wired::before { content: ""; }
.fa-neuter::before { content: ""; }
.fa-newspaper::before { content: ""; }
.fa-nimblr::before { content: ""; }
.fa-node::before { content: ""; }
.fa-node-js::before { content: ""; }
.fa-not-equal::before { content: ""; }
.fa-notes-medical::before { content: ""; }
.fa-npm::before { content: ""; }
.fa-ns8::before { content: ""; }
.fa-nutritionix::before { content: ""; }
.fa-object-group::before { content: ""; }
.fa-object-ungroup::before { content: ""; }
.fa-octopus-deploy::before { content: ""; }
.fa-odnoklassniki::before { content: ""; }
.fa-odnoklassniki-square::before { content: ""; }
.fa-oil-can::before { content: ""; }
.fa-old-republic::before { content: ""; }
.fa-om::before { content: ""; }
.fa-opencart::before { content: ""; }
.fa-openid::before { content: ""; }
.fa-opera::before { content: ""; }
.fa-optin-monster::before { content: ""; }
.fa-orcid::before { content: ""; }
.fa-osi::before { content: ""; }
.fa-otter::before { content: ""; }
.fa-outdent::before { content: ""; }
.fa-page4::before { content: ""; }
.fa-pagelines::before { content: ""; }
.fa-pager::before { content: ""; }
.fa-paint-brush::before { content: ""; }
.fa-paint-roller::before { content: ""; }
.fa-palette::before { content: ""; }
.fa-palfed::before { content: ""; }
.fa-pallet::before { content: ""; }
.fa-paper-plane::before { content: ""; }
.fa-paperclip::before { content: ""; }
.fa-parachute-box::before { content: ""; }
.fa-paragraph::before { content: ""; }
.fa-parking::before { content: ""; }
.fa-passport::before { content: ""; }
.fa-pastafarianism::before { content: ""; }
.fa-paste::before { content: ""; }
.fa-patreon::before { content: ""; }
.fa-pause::before { content: ""; }
.fa-pause-circle::before { content: ""; }
.fa-paw::before { content: ""; }
.fa-paypal::before { content: ""; }
.fa-peace::before { content: ""; }
.fa-pen::before { content: ""; }
.fa-pen-alt::before { content: ""; }
.fa-pen-fancy::before { content: ""; }
.fa-pen-nib::before { content: ""; }
.fa-pen-square::before { content: ""; }
.fa-pencil-alt::before { content: ""; }
.fa-pencil-ruler::before { content: ""; }
.fa-penny-arcade::before { content: ""; }
.fa-people-arrows::before { content: ""; }
.fa-people-carry::before { content: ""; }
.fa-pepper-hot::before { content: ""; }
.fa-perbyte::before { content: ""; }
.fa-percent::before { content: ""; }
.fa-percentage::before { content: ""; }
.fa-periscope::before { content: ""; }
.fa-person-booth::before { content: ""; }
.fa-phabricator::before { content: ""; }
.fa-phoenix-framework::before { content: ""; }
.fa-phoenix-squadron::before { content: ""; }
.fa-phone::before { content: ""; }
.fa-phone-alt::before { content: ""; }
.fa-phone-slash::before { content: ""; }
.fa-phone-square::before { content: ""; }
.fa-phone-square-alt::before { content: ""; }
.fa-phone-volume::before { content: ""; }
.fa-photo-video::before { content: ""; }
.fa-php::before { content: ""; }
.fa-pied-piper::before { content: ""; }
.fa-pied-piper-alt::before { content: ""; }
.fa-pied-piper-hat::before { content: ""; }
.fa-pied-piper-pp::before { content: ""; }
.fa-pied-piper-square::before { content: ""; }
.fa-piggy-bank::before { content: ""; }
.fa-pills::before { content: ""; }
.fa-pinterest::before { content: ""; }
.fa-pinterest-p::before { content: ""; }
.fa-pinterest-square::before { content: ""; }
.fa-pizza-slice::before { content: ""; }
.fa-place-of-worship::before { content: ""; }
.fa-plane::before { content: ""; }
.fa-plane-arrival::before { content: ""; }
.fa-plane-departure::before { content: ""; }
.fa-plane-slash::before { content: ""; }
.fa-play::before { content: ""; }
.fa-play-circle::before { content: ""; }
.fa-playstation::before { content: ""; }
.fa-plug::before { content: ""; }
.fa-plus::before { content: ""; }
.fa-plus-circle::before { content: ""; }
.fa-plus-square::before { content: ""; }
.fa-podcast::before { content: ""; }
.fa-poll::before { content: ""; }
.fa-poll-h::before { content: ""; }
.fa-poo::before { content: ""; }
.fa-poo-storm::before { content: ""; }
.fa-poop::before { content: ""; }
.fa-portrait::before { content: ""; }
.fa-pound-sign::before { content: ""; }
.fa-power-off::before { content: ""; }
.fa-pray::before { content: ""; }
.fa-praying-hands::before { content: ""; }
.fa-prescription::before { content: ""; }
.fa-prescription-bottle::before { content: ""; }
.fa-prescription-bottle-alt::before { content: ""; }
.fa-print::before { content: ""; }
.fa-procedures::before { content: ""; }
.fa-product-hunt::before { content: ""; }
.fa-project-diagram::before { content: ""; }
.fa-pump-medical::before { content: ""; }
.fa-pump-soap::before { content: ""; }
.fa-pushed::before { content: ""; }
.fa-puzzle-piece::before { content: ""; }
.fa-python::before { content: ""; }
.fa-qq::before { content: ""; }
.fa-qrcode::before { content: ""; }
.fa-question::before { content: ""; }
.fa-question-circle::before { content: ""; }
.fa-quidditch::before { content: ""; }
.fa-quinscape::before { content: ""; }
.fa-quora::before { content: ""; }
.fa-quote-left::before { content: ""; }
.fa-quote-right::before { content: ""; }
.fa-quran::before { content: ""; }
.fa-r-project::before { content: ""; }
.fa-radiation::before { content: ""; }
.fa-radiation-alt::before { content: ""; }
.fa-rainbow::before { content: ""; }
.fa-random::before { content: ""; }
.fa-raspberry-pi::before { content: ""; }
.fa-ravelry::before { content: ""; }
.fa-react::before { content: ""; }
.fa-reacteurope::before { content: ""; }
.fa-readme::before { content: ""; }
.fa-rebel::before { content: ""; }
.fa-receipt::before { content: ""; }
.fa-record-vinyl::before { content: ""; }
.fa-recycle::before { content: ""; }
.fa-red-river::before { content: ""; }
.fa-reddit::before { content: ""; }
.fa-reddit-alien::before { content: ""; }
.fa-reddit-square::before { content: ""; }
.fa-redhat::before { content: ""; }
.fa-redo::before { content: ""; }
.fa-redo-alt::before { content: ""; }
.fa-registered::before { content: ""; }
.fa-remove-format::before { content: ""; }
.fa-renren::before { content: ""; }
.fa-reply::before { content: ""; }
.fa-reply-all::before { content: ""; }
.fa-replyd::before { content: ""; }
.fa-republican::before { content: ""; }
.fa-researchgate::before { content: ""; }
.fa-resolving::before { content: ""; }
.fa-restroom::before { content: ""; }
.fa-retweet::before { content: ""; }
.fa-rev::before { content: ""; }
.fa-ribbon::before { content: ""; }
.fa-ring::before { content: ""; }
.fa-road::before { content: ""; }
.fa-robot::before { content: ""; }
.fa-rocket::before { content: ""; }
.fa-rocketchat::before { content: ""; }
.fa-rockrms::before { content: ""; }
.fa-route::before { content: ""; }
.fa-rss::before { content: ""; }
.fa-rss-square::before { content: ""; }
.fa-ruble-sign::before { content: ""; }
.fa-ruler::before { content: ""; }
.fa-ruler-combined::before { content: ""; }
.fa-ruler-horizontal::before { content: ""; }
.fa-ruler-vertical::before { content: ""; }
.fa-running::before { content: ""; }
.fa-rupee-sign::before { content: ""; }
.fa-rust::before { content: ""; }
.fa-sad-cry::before { content: ""; }
.fa-sad-tear::before { content: ""; }
.fa-safari::before { content: ""; }
.fa-salesforce::before { content: ""; }
.fa-sass::before { content: ""; }
.fa-satellite::before { content: ""; }
.fa-satellite-dish::before { content: ""; }
.fa-save::before { content: ""; }
.fa-schlix::before { content: ""; }
.fa-school::before { content: ""; }
.fa-screwdriver::before { content: ""; }
.fa-scribd::before { content: ""; }
.fa-scroll::before { content: ""; }
.fa-sd-card::before { content: ""; }
.fa-search::before { content: ""; }
.fa-search-dollar::before { content: ""; }
.fa-search-location::before { content: ""; }
.fa-search-minus::before { content: ""; }
.fa-search-plus::before { content: ""; }
.fa-searchengin::before { content: ""; }
.fa-seedling::before { content: ""; }
.fa-sellcast::before { content: ""; }
.fa-sellsy::before { content: ""; }
.fa-server::before { content: ""; }
.fa-servicestack::before { content: ""; }
.fa-shapes::before { content: ""; }
.fa-share::before { content: ""; }
.fa-share-alt::before { content: ""; }
.fa-share-alt-square::before { content: ""; }
.fa-share-square::before { content: ""; }
.fa-shekel-sign::before { content: ""; }
.fa-shield-alt::before { content: ""; }
.fa-shield-virus::before { content: ""; }
.fa-ship::before { content: ""; }
.fa-shipping-fast::before { content: ""; }
.fa-shirtsinbulk::before { content: ""; }
.fa-shoe-prints::before { content: ""; }
.fa-shopify::before { content: ""; }
.fa-shopping-bag::before { content: ""; }
.fa-shopping-basket::before { content: ""; }
.fa-shopping-cart::before { content: ""; }
.fa-shopware::before { content: ""; }
.fa-shower::before { content: ""; }
.fa-shuttle-van::before { content: ""; }
.fa-sign::before { content: ""; }
.fa-sign-in-alt::before { content: ""; }
.fa-sign-language::before { content: ""; }
.fa-sign-out-alt::before { content: ""; }
.fa-signal::before { content: ""; }
.fa-signature::before { content: ""; }
.fa-sim-card::before { content: ""; }
.fa-simplybuilt::before { content: ""; }
.fa-sink::before { content: ""; }
.fa-sistrix::before { content: ""; }
.fa-sitemap::before { content: ""; }
.fa-sith::before { content: ""; }
.fa-skating::before { content: ""; }
.fa-sketch::before { content: ""; }
.fa-skiing::before { content: ""; }
.fa-skiing-nordic::before { content: ""; }
.fa-skull::before { content: ""; }
.fa-skull-crossbones::before { content: ""; }
.fa-skyatlas::before { content: ""; }
.fa-skype::before { content: ""; }
.fa-slack::before { content: ""; }
.fa-slack-hash::before { content: ""; }
.fa-slash::before { content: ""; }
.fa-sleigh::before { content: ""; }
.fa-sliders-h::before { content: ""; }
.fa-slideshare::before { content: ""; }
.fa-smile::before { content: ""; }
.fa-smile-beam::before { content: ""; }
.fa-smile-wink::before { content: ""; }
.fa-smog::before { content: ""; }
.fa-smoking::before { content: ""; }
.fa-smoking-ban::before { content: ""; }
.fa-sms::before { content: ""; }
.fa-snapchat::before { content: ""; }
.fa-snapchat-ghost::before { content: ""; }
.fa-snapchat-square::before { content: ""; }
.fa-snowboarding::before { content: ""; }
.fa-snowflake::before { content: ""; }
.fa-snowman::before { content: ""; }
.fa-snowplow::before { content: ""; }
.fa-soap::before { content: ""; }
.fa-socks::before { content: ""; }
.fa-solar-panel::before { content: ""; }
.fa-sort::before { content: ""; }
.fa-sort-alpha-down::before { content: ""; }
.fa-sort-alpha-down-alt::before { content: ""; }
.fa-sort-alpha-up::before { content: ""; }
.fa-sort-alpha-up-alt::before { content: ""; }
.fa-sort-amount-down::before { content: ""; }
.fa-sort-amount-down-alt::before { content: ""; }
.fa-sort-amount-up::before { content: ""; }
.fa-sort-amount-up-alt::before { content: ""; }
.fa-sort-down::before { content: ""; }
.fa-sort-numeric-down::before { content: ""; }
.fa-sort-numeric-down-alt::before { content: ""; }
.fa-sort-numeric-up::before { content: ""; }
.fa-sort-numeric-up-alt::before { content: ""; }
.fa-sort-up::before { content: ""; }
.fa-soundcloud::before { content: ""; }
.fa-sourcetree::before { content: ""; }
.fa-spa::before { content: ""; }
.fa-space-shuttle::before { content: ""; }
.fa-speakap::before { content: ""; }
.fa-speaker-deck::before { content: ""; }
.fa-spell-check::before { content: ""; }
.fa-spider::before { content: ""; }
.fa-spinner::before { content: ""; }
.fa-splotch::before { content: ""; }
.fa-spotify::before { content: ""; }
.fa-spray-can::before { content: ""; }
.fa-square::before { content: ""; }
.fa-square-full::before { content: ""; }
.fa-square-root-alt::before { content: ""; }
.fa-squarespace::before { content: ""; }
.fa-stack-exchange::before { content: ""; }
.fa-stack-overflow::before { content: ""; }
.fa-stackpath::before { content: ""; }
.fa-stamp::before { content: ""; }
.fa-star::before { content: ""; }
.fa-star-and-crescent::before { content: ""; }
.fa-star-half::before { content: ""; }
.fa-star-half-alt::before { content: ""; }
.fa-star-of-david::before { content: ""; }
.fa-star-of-life::before { content: ""; }
.fa-staylinked::before { content: ""; }
.fa-steam::before { content: ""; }
.fa-steam-square::before { content: ""; }
.fa-steam-symbol::before { content: ""; }
.fa-step-backward::before { content: ""; }
.fa-step-forward::before { content: ""; }
.fa-stethoscope::before { content: ""; }
.fa-sticker-mule::before { content: ""; }
.fa-sticky-note::before { content: ""; }
.fa-stop::before { content: ""; }
.fa-stop-circle::before { content: ""; }
.fa-stopwatch::before { content: ""; }
.fa-stopwatch-20::before { content: ""; }
.fa-store::before { content: ""; }
.fa-store-alt::before { content: ""; }
.fa-store-alt-slash::before { content: ""; }
.fa-store-slash::before { content: ""; }
.fa-strava::before { content: ""; }
.fa-stream::before { content: ""; }
.fa-street-view::before { content: ""; }
.fa-strikethrough::before { content: ""; }
.fa-stripe::before { content: ""; }
.fa-stripe-s::before { content: ""; }
.fa-stroopwafel::before { content: ""; }
.fa-studiovinari::before { content: ""; }
.fa-stumbleupon::before { content: ""; }
.fa-stumbleupon-circle::before { content: ""; }
.fa-subscript::before { content: ""; }
.fa-subway::before { content: ""; }
.fa-suitcase::before { content: ""; }
.fa-suitcase-rolling::before { content: ""; }
.fa-sun::before { content: ""; }
.fa-superpowers::before { content: ""; }
.fa-superscript::before { content: ""; }
.fa-supple::before { content: ""; }
.fa-surprise::before { content: ""; }
.fa-suse::before { content: ""; }
.fa-swatchbook::before { content: ""; }
.fa-swift::before { content: ""; }
.fa-swimmer::before { content: ""; }
.fa-swimming-pool::before { content: ""; }
.fa-symfony::before { content: ""; }
.fa-synagogue::before { content: ""; }
.fa-sync::before { content: ""; }
.fa-sync-alt::before { content: ""; }
.fa-syringe::before { content: ""; }
.fa-table::before { content: ""; }
.fa-table-tennis::before { content: ""; }
.fa-tablet::before { content: ""; }
.fa-tablet-alt::before { content: ""; }
.fa-tablets::before { content: ""; }
.fa-tachometer-alt::before { content: ""; }
.fa-tag::before { content: ""; }
.fa-tags::before { content: ""; }
.fa-tape::before { content: ""; }
.fa-tasks::before { content: ""; }
.fa-taxi::before { content: ""; }
.fa-teamspeak::before { content: ""; }
.fa-teeth::before { content: ""; }
.fa-teeth-open::before { content: ""; }
.fa-telegram::before { content: ""; }
.fa-telegram-plane::before { content: ""; }
.fa-temperature-high::before { content: ""; }
.fa-temperature-low::before { content: ""; }
.fa-tencent-weibo::before { content: ""; }
.fa-tenge::before { content: ""; }
.fa-terminal::before { content: ""; }
.fa-text-height::before { content: ""; }
.fa-text-width::before { content: ""; }
.fa-th::before { content: ""; }
.fa-th-large::before { content: ""; }
.fa-th-list::before { content: ""; }
.fa-the-red-yeti::before { content: ""; }
.fa-theater-masks::before { content: ""; }
.fa-themeco::before { content: ""; }
.fa-themeisle::before { content: ""; }
.fa-thermometer::before { content: ""; }
.fa-thermometer-empty::before { content: ""; }
.fa-thermometer-full::before { content: ""; }
.fa-thermometer-half::before { content: ""; }
.fa-thermometer-quarter::before { content: ""; }
.fa-thermometer-three-quarters::before { content: ""; }
.fa-think-peaks::before { content: ""; }
.fa-thumbs-down::before { content: ""; }
.fa-thumbs-up::before { content: ""; }
.fa-thumbtack::before { content: ""; }
.fa-ticket-alt::before { content: ""; }
.fa-tiktok::before { content: ""; }
.fa-times::before { content: ""; }
.fa-times-circle::before { content: ""; }
.fa-tint::before { content: ""; }
.fa-tint-slash::before { content: ""; }
.fa-tired::before { content: ""; }
.fa-toggle-off::before { content: ""; }
.fa-toggle-on::before { content: ""; }
.fa-toilet::before { content: ""; }
.fa-toilet-paper::before { content: ""; }
.fa-toilet-paper-slash::before { content: ""; }
.fa-toolbox::before { content: ""; }
.fa-tools::before { content: ""; }
.fa-tooth::before { content: ""; }
.fa-torah::before { content: ""; }
.fa-torii-gate::before { content: ""; }
.fa-tractor::before { content: ""; }
.fa-trade-federation::before { content: ""; }
.fa-trademark::before { content: ""; }
.fa-traffic-light::before { content: ""; }
.fa-trailer::before { content: ""; }
.fa-train::before { content: ""; }
.fa-tram::before { content: ""; }
.fa-transgender::before { content: ""; }
.fa-transgender-alt::before { content: ""; }
.fa-trash::before { content: ""; }
.fa-trash-alt::before { content: ""; }
.fa-trash-restore::before { content: ""; }
.fa-trash-restore-alt::before { content: ""; }
.fa-tree::before { content: ""; }
.fa-trello::before { content: ""; }
.fa-tripadvisor::before { content: ""; }
.fa-trophy::before { content: ""; }
.fa-truck::before { content: ""; }
.fa-truck-loading::before { content: ""; }
.fa-truck-monster::before { content: ""; }
.fa-truck-moving::before { content: ""; }
.fa-truck-pickup::before { content: ""; }
.fa-tshirt::before { content: ""; }
.fa-tty::before { content: ""; }
.fa-tumblr::before { content: ""; }
.fa-tumblr-square::before { content: ""; }
.fa-tv::before { content: ""; }
.fa-twitch::before { content: ""; }
.fa-twitter::before { content: ""; }
.fa-twitter-square::before { content: ""; }
.fa-typo3::before { content: ""; }
.fa-uber::before { content: ""; }
.fa-ubuntu::before { content: ""; }
.fa-uikit::before { content: ""; }
.fa-umbraco::before { content: ""; }
.fa-umbrella::before { content: ""; }
.fa-umbrella-beach::before { content: ""; }
.fa-uncharted::before { content: ""; }
.fa-underline::before { content: ""; }
.fa-undo::before { content: ""; }
.fa-undo-alt::before { content: ""; }
.fa-uniregistry::before { content: ""; }
.fa-unity::before { content: ""; }
.fa-universal-access::before { content: ""; }
.fa-university::before { content: ""; }
.fa-unlink::before { content: ""; }
.fa-unlock::before { content: ""; }
.fa-unlock-alt::before { content: ""; }
.fa-unsplash::before { content: ""; }
.fa-untappd::before { content: ""; }
.fa-upload::before { content: ""; }
.fa-ups::before { content: ""; }
.fa-usb::before { content: ""; }
.fa-user::before { content: ""; }
.fa-user-alt::before { content: ""; }
.fa-user-alt-slash::before { content: ""; }
.fa-user-astronaut::before { content: ""; }
.fa-user-check::before { content: ""; }
.fa-user-circle::before { content: ""; }
.fa-user-clock::before { content: ""; }
.fa-user-cog::before { content: ""; }
.fa-user-edit::before { content: ""; }
.fa-user-friends::before { content: ""; }
.fa-user-graduate::before { content: ""; }
.fa-user-injured::before { content: ""; }
.fa-user-lock::before { content: ""; }
.fa-user-md::before { content: ""; }
.fa-user-minus::before { content: ""; }
.fa-user-ninja::before { content: ""; }
.fa-user-nurse::before { content: ""; }
.fa-user-plus::before { content: ""; }
.fa-user-secret::before { content: ""; }
.fa-user-shield::before { content: ""; }
.fa-user-slash::before { content: ""; }
.fa-user-tag::before { content: ""; }
.fa-user-tie::before { content: ""; }
.fa-user-times::before { content: ""; }
.fa-users::before { content: ""; }
.fa-users-cog::before { content: ""; }
.fa-users-slash::before { content: ""; }
.fa-usps::before { content: ""; }
.fa-ussunnah::before { content: ""; }
.fa-utensil-spoon::before { content: ""; }
.fa-utensils::before { content: ""; }
.fa-vaadin::before { content: ""; }
.fa-vector-square::before { content: ""; }
.fa-venus::before { content: ""; }
.fa-venus-double::before { content: ""; }
.fa-venus-mars::before { content: ""; }
.fa-vest::before { content: ""; }
.fa-vest-patches::before { content: ""; }
.fa-viacoin::before { content: ""; }
.fa-viadeo::before { content: ""; }
.fa-viadeo-square::before { content: ""; }
.fa-vial::before { content: ""; }
.fa-vials::before { content: ""; }
.fa-viber::before { content: ""; }
.fa-video::before { content: ""; }
.fa-video-slash::before { content: ""; }
.fa-vihara::before { content: ""; }
.fa-vimeo::before { content: ""; }
.fa-vimeo-square::before { content: ""; }
.fa-vimeo-v::before { content: ""; }
.fa-vine::before { content: ""; }
.fa-virus::before { content: ""; }
.fa-virus-slash::before { content: ""; }
.fa-viruses::before { content: ""; }
.fa-vk::before { content: ""; }
.fa-vnv::before { content: ""; }
.fa-voicemail::before { content: ""; }
.fa-volleyball-ball::before { content: ""; }
.fa-volume-down::before { content: ""; }
.fa-volume-mute::before { content: ""; }
.fa-volume-off::before { content: ""; }
.fa-volume-up::before { content: ""; }
.fa-vote-yea::before { content: ""; }
.fa-vr-cardboard::before { content: ""; }
.fa-vuejs::before { content: ""; }
.fa-walking::before { content: ""; }
.fa-wallet::before { content: ""; }
.fa-warehouse::before { content: ""; }
.fa-watchman-monitoring::before { content: ""; }
.fa-water::before { content: ""; }
.fa-wave-square::before { content: ""; }
.fa-waze::before { content: ""; }
.fa-weebly::before { content: ""; }
.fa-weibo::before { content: ""; }
.fa-weight::before { content: ""; }
.fa-weight-hanging::before { content: ""; }
.fa-weixin::before { content: ""; }
.fa-whatsapp::before { content: ""; }
.fa-whatsapp-square::before { content: ""; }
.fa-wheelchair::before { content: ""; }
.fa-whmcs::before { content: ""; }
.fa-wifi::before { content: ""; }
.fa-wikipedia-w::before { content: ""; }
.fa-wind::before { content: ""; }
.fa-window-close::before { content: ""; }
.fa-window-maximize::before { content: ""; }
.fa-window-minimize::before { content: ""; }
.fa-window-restore::before { content: ""; }
.fa-windows::before { content: ""; }
.fa-wine-bottle::before { content: ""; }
.fa-wine-glass::before { content: ""; }
.fa-wine-glass-alt::before { content: ""; }
.fa-wix::before { content: ""; }
.fa-wizards-of-the-coast::before { content: ""; }
.fa-wodu::before { content: ""; }
.fa-wolf-pack-battalion::before { content: ""; }
.fa-won-sign::before { content: ""; }
.fa-wordpress::before { content: ""; }
.fa-wordpress-simple::before { content: ""; }
.fa-wpbeginner::before { content: ""; }
.fa-wpexplorer::before { content: ""; }
.fa-wpforms::before { content: ""; }
.fa-wpressr::before { content: ""; }
.fa-wrench::before { content: ""; }
.fa-x-ray::before { content: ""; }
.fa-xbox::before { content: ""; }
.fa-xing::before { content: ""; }
.fa-xing-square::before { content: ""; }
.fa-y-combinator::before { content: ""; }
.fa-yahoo::before { content: ""; }
.fa-yammer::before { content: ""; }
.fa-yandex::before { content: ""; }
.fa-yandex-international::before { content: ""; }
.fa-yarn::before { content: ""; }
.fa-yelp::before { content: ""; }
.fa-yen-sign::before { content: ""; }
.fa-yin-yang::before { content: ""; }
.fa-yoast::before { content: ""; }
.fa-youtube::before { content: ""; }
.fa-youtube-square::before { content: ""; }
.fa-zhihu::before { content: ""; }
.sr-only { border: 0px; clip: rect(0px, 0px, 0px, 0px); height: 1px; margin: -1px; overflow: hidden; padding: 0px; position: absolute; width: 1px; }
.sr-only-focusable:active, .sr-only-focusable:focus { clip: auto; height: auto; margin: 0px; overflow: visible; position: static; width: auto; }
@font-face { font-family: "Font Awesome 5 Brands"; font-style: normal; font-weight: 400; font-display: block; src: url("../webfonts/fa-brands-400.woff2") format("woff2"), url("../webfonts/fa-brands-400.woff") format("woff"), url("../webfonts/fa-brands-400.ttf") format("truetype"); }
.fab { font-family: "Font Awesome 5 Brands"; }
@font-face { font-family: "Font Awesome 5 Free"; font-style: normal; font-weight: 400; font-display: block; src: url("../webfonts/fa-regular-400.woff2") format("woff2"), url("../webfonts/fa-regular-400.woff") format("woff"), url("../webfonts/fa-regular-400.ttf") format("truetype"); }
.fab, .far { font-weight: 400; }
@font-face { font-family: "Font Awesome 5 Free"; font-style: normal; font-weight: 900; font-display: block; src: url("../webfonts/fa-solid-900.woff2") format("woff2"), url("../webfonts/fa-solid-900.woff") format("woff"), url("../webfonts/fa-solid-900.ttf") format("truetype"); }
.fa, .far, .fas { font-family: "Font Awesome 5 Free"; }
.fa, .fas { font-weight: 900; }
:root { --blue: #4e73df; --indigo: #6610f2; --purple: #6f42c1; --pink: #e83e8c; --red: #e74a3b; --orange: #fd7e14; --yellow: #f6c23e; --green: #1cc88a; --teal: #20c9a6; --cyan: #36b9cc; --white: #fff; --gray: #858796; --gray-dark: #5a5c69; --primary: #4e73df; --secondary: #858796; --success: #1cc88a; --info: #36b9cc; --warning: #f6c23e; --danger: #e74a3b; --light: #f8f9fc; --dark: #5a5c69; --breakpoint-xs: 0; --breakpoint-sm: 576px; --breakpoint-md: 768px; --breakpoint-lg: 992px; --breakpoint-xl: 1200px; --font-family-sans-serif: "Nunito",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"; --font-family-monospace: SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace; }
*, ::after, ::before { box-sizing: border-box; }
html { font-family: sans-serif; line-height: 1.15; text-size-adjust: 100%; -webkit-tap-highlight-color: transparent; }
article, aside, figcaption, figure, footer, header, hgroup, main, nav, section { display: block; }
body { margin: 0px; font-family: Nunito, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"; font-size: 1rem; font-weight: 400; line-height: 1.5; color: rgb(133, 135, 150); text-align: left; background-color: rgb(255, 255, 255); }
[tabindex="-1"]:focus:not(:focus-visible) { outline: 0px !important; }
hr { box-sizing: content-box; height: 0px; overflow: visible; }
h1, h2, h3, h4, h5, h6 { margin-top: 0px; margin-bottom: 0.5rem; }
p { margin-top: 0px; margin-bottom: 1rem; }
abbr[data-original-title], abbr[title] { text-decoration: underline dotted; cursor: help; border-bottom: 0px; text-decoration-skip-ink: none; }
address { margin-bottom: 1rem; font-style: normal; line-height: inherit; }
dl, ol, ul { margin-top: 0px; margin-bottom: 1rem; }
ol ol, ol ul, ul ol, ul ul { margin-bottom: 0px; }
dt { font-weight: 700; }
dd { margin-bottom: 0.5rem; margin-left: 0px; }
blockquote { margin: 0px 0px 1rem; }
b, strong { font-weight: bolder; }
small { font-size: 80%; }
sub, sup { position: relative; font-size: 75%; line-height: 0; vertical-align: baseline; }
sub { bottom: -0.25em; }
sup { top: -0.5em; }
a { color: rgb(78, 115, 223); text-decoration: none; background-color: transparent; }
a:hover { color: rgb(34, 74, 190); text-decoration: underline; }
a:not([href]):not([class]) { color: inherit; text-decoration: none; }
a:not([href]):not([class]):hover { color: inherit; text-decoration: none; }
code, kbd, pre, samp { font-family: SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; font-size: 1em; }
pre { margin-top: 0px; margin-bottom: 1rem; overflow: auto; }
figure { margin: 0px 0px 1rem; }
img { vertical-align: middle; border-style: none; }
svg { overflow: hidden; vertical-align: middle; }
table { border-collapse: collapse; }
caption { padding-top: 0.75rem; padding-bottom: 0.75rem; color: rgb(133, 135, 150); text-align: left; caption-side: bottom; }
th { text-align: -webkit-match-parent; }
label { display: inline-block; margin-bottom: 0.5rem; }
button { border-radius: 0px; }
button:focus:not(:focus-visible) { outline: 0px; }
button, input, optgroup, select, textarea { margin: 0px; font-family: inherit; font-size: inherit; line-height: inherit; }
button, input { overflow: visible; }
button, select { text-transform: none; }
[role="button"] { cursor: pointer; }
select { overflow-wrap: normal; }
[type="button"], [type="reset"], [type="submit"], button { appearance: button; }
[type="button"]:not(:disabled), [type="reset"]:not(:disabled), [type="submit"]:not(:disabled), button:not(:disabled) { cursor: pointer; }
input[type="checkbox"], input[type="radio"] { box-sizing: border-box; padding: 0px; }
textarea { overflow: auto; resize: vertical; }
fieldset { min-width: 0px; padding: 0px; margin: 0px; border: 0px; }
legend { display: block; width: 100%; max-width: 100%; padding: 0px; margin-bottom: 0.5rem; font-size: 1.5rem; line-height: inherit; color: inherit; white-space: normal; }
progress { vertical-align: baseline; }
[type="number"]::-webkit-inner-spin-button, [type="number"]::-webkit-outer-spin-button { height: auto; }
[type="search"] { outline-offset: -2px; appearance: none; }
[type="search"]::-webkit-search-decoration { appearance: none; }
::-webkit-file-upload-button { font: inherit; appearance: button; }
output { display: inline-block; }
summary { display: list-item; cursor: pointer; }
template { display: none; }
[hidden] { display: none !important; }
.h1, .h2, .h3, .h4, .h5, .h6, h1, h2, h3, h4, h5, h6 { margin-bottom: 0.5rem; font-weight: 400; line-height: 1.2; }
.h1, h1 { font-size: 2.5rem; }
.h2, h2 { font-size: 2rem; }
.h3, h3 { font-size: 1.75rem; }
.h4, h4 { font-size: 1.5rem; }
.h5, h5 { font-size: 1.25rem; }
.h6, h6 { font-size: 1rem; }
.lead { font-size: 1.25rem; font-weight: 300; }
.display-1 { font-size: 6rem; font-weight: 300; line-height: 1.2; }
.display-2 { font-size: 5.5rem; font-weight: 300; line-height: 1.2; }
.display-3 { font-size: 4.5rem; font-weight: 300; line-height: 1.2; }
.display-4 { font-size: 3.5rem; font-weight: 300; line-height: 1.2; }
hr { margin-top: 1rem; margin-bottom: 1rem; border-width: 1px 0px 0px; border-right-style: initial; border-bottom-style: initial; border-left-style: initial; border-right-color: initial; border-bottom-color: initial; border-left-color: initial; border-image: initial; border-top-style: solid; border-top-color: rgba(0, 0, 0, 0.1); }
.small, small { font-size: 80%; font-weight: 400; }
.mark, mark { padding: 0.2em; background-color: rgb(252, 248, 227); }
.list-unstyled { padding-left: 0px; list-style: none; }
.list-inline { padding-left: 0px; list-style: none; }
.list-inline-item { display: inline-block; }
.list-inline-item:not(:last-child) { margin-right: 0.5rem; }
.initialism { font-size: 90%; text-transform: uppercase; }
.blockquote { margin-bottom: 1rem; font-size: 1.25rem; }
.blockquote-footer { display: block; font-size: 80%; color: rgb(133, 135, 150); }
.blockquote-footer::before { content: "— "; }
.img-fluid { max-width: 100%; height: auto; }
.img-thumbnail { padding: 0.25rem; background-color: rgb(255, 255, 255); border: 1px solid rgb(221, 223, 235); border-radius: 0.35rem; max-width: 100%; height: auto; }
.figure { display: inline-block; }
.figure-img { margin-bottom: 0.5rem; line-height: 1; }
.figure-caption { font-size: 90%; color: rgb(133, 135, 150); }
code { font-size: 87.5%; color: rgb(232, 62, 140); overflow-wrap: break-word; }
a > code { color: inherit; }
kbd { padding: 0.2rem 0.4rem; font-size: 87.5%; color: rgb(255, 255, 255); background-color: rgb(58, 59, 69); border-radius: 0.2rem; }
kbd kbd { padding: 0px; font-size: 100%; font-weight: 700; }
pre { display: block; font-size: 87.5%; color: rgb(58, 59, 69); }
pre code { font-size: inherit; color: inherit; word-break: normal; }
.pre-scrollable { max-height: 340px; overflow-y: scroll; }
.container, .container-fluid, .container-lg, .container-md, .container-sm, .container-xl { width: 100%; padding-right: 0.75rem; padding-left: 0.75rem; margin-right: auto; margin-left: auto; }
@media (min-width: 576px) {
  .container, .container-sm { max-width: 540px; }
}
@media (min-width: 768px) {
  .container, .container-md, .container-sm { max-width: 720px; }
}
@media (min-width: 992px) {
  .container, .container-lg, .container-md, .container-sm { max-width: 960px; }
}
@media (min-width: 1200px) {
  .container, .container-lg, .container-md, .container-sm, .container-xl { max-width: 1140px; }
}
.row { display: flex; flex-wrap: wrap; margin-right: -0.75rem; margin-left: -0.75rem; }
.no-gutters { margin-right: 0px; margin-left: 0px; }
.no-gutters > .col, .no-gutters > [class*="col-"] { padding-right: 0px; padding-left: 0px; }
.col, .col-1, .col-10, .col-11, .col-12, .col-2, .col-3, .col-4, .col-5, .col-6, .col-7, .col-8, .col-9, .col-auto, .col-lg, .col-lg-1, .col-lg-10, .col-lg-11, .col-lg-12, .col-lg-2, .col-lg-3, .col-lg-4, .col-lg-5, .col-lg-6, .col-lg-7, .col-lg-8, .col-lg-9, .col-lg-auto, .col-md, .col-md-1, .col-md-10, .col-md-11, .col-md-12, .col-md-2, .col-md-3, .col-md-4, .col-md-5, .col-md-6, .col-md-7, .col-md-8, .col-md-9, .col-md-auto, .col-sm, .col-sm-1, .col-sm-10, .col-sm-11, .col-sm-12, .col-sm-2, .col-sm-3, .col-sm-4, .col-sm-5, .col-sm-6, .col-sm-7, .col-sm-8, .col-sm-9, .col-sm-auto, .col-xl, .col-xl-1, .col-xl-10, .col-xl-11, .col-xl-12, .col-xl-2, .col-xl-3, .col-xl-4, .col-xl-5, .col-xl-6, .col-xl-7, .col-xl-8, .col-xl-9, .col-xl-auto { position: relative; width: 100%; padding-right: 0.75rem; padding-left: 0.75rem; }
.col { flex-basis: 0px; flex-grow: 1; max-width: 100%; }
.row-cols-1 > * { flex: 0 0 100%; max-width: 100%; }
.row-cols-2 > * { flex: 0 0 50%; max-width: 50%; }
.row-cols-3 > * { flex: 0 0 33.3333%; max-width: 33.3333%; }
.row-cols-4 > * { flex: 0 0 25%; max-width: 25%; }
.row-cols-5 > * { flex: 0 0 20%; max-width: 20%; }
.row-cols-6 > * { flex: 0 0 16.6667%; max-width: 16.6667%; }
.col-auto { flex: 0 0 auto; width: auto; max-width: 100%; }
.col-1 { flex: 0 0 8.33333%; max-width: 8.33333%; }
.col-2 { flex: 0 0 16.6667%; max-width: 16.6667%; }
.col-3 { flex: 0 0 25%; max-width: 25%; }
.col-4 { flex: 0 0 33.3333%; max-width: 33.3333%; }
.col-5 { flex: 0 0 41.6667%; max-width: 41.6667%; }
.col-6 { flex: 0 0 50%; max-width: 50%; }
.col-7 { flex: 0 0 58.3333%; max-width: 58.3333%; }
.col-8 { flex: 0 0 66.6667%; max-width: 66.6667%; }
.col-9 { flex: 0 0 75%; max-width: 75%; }
.col-10 { flex: 0 0 83.3333%; max-width: 83.3333%; }
.col-11 { flex: 0 0 91.6667%; max-width: 91.6667%; }
.col-12 { flex: 0 0 100%; max-width: 100%; }
.order-first { order: -1; }
.order-last { order: 13; }
.order-0 { order: 0; }
.order-1 { order: 1; }
.order-2 { order: 2; }
.order-3 { order: 3; }
.order-4 { order: 4; }
.order-5 { order: 5; }
.order-6 { order: 6; }
.order-7 { order: 7; }
.order-8 { order: 8; }
.order-9 { order: 9; }
.order-10 { order: 10; }
.order-11 { order: 11; }
.order-12 { order: 12; }
.offset-1 { margin-left: 8.33333%; }
.offset-2 { margin-left: 16.6667%; }
.offset-3 { margin-left: 25%; }
.offset-4 { margin-left: 33.3333%; }
.offset-5 { margin-left: 41.6667%; }
.offset-6 { margin-left: 50%; }
.offset-7 { margin-left: 58.3333%; }
.offset-8 { margin-left: 66.6667%; }
.offset-9 { margin-left: 75%; }
.offset-10 { margin-left: 83.3333%; }
.offset-11 { margin-left: 91.6667%; }
@media (min-width: 576px) {
  .col-sm { flex-basis: 0px; flex-grow: 1; max-width: 100%; }
  .row-cols-sm-1 > * { flex: 0 0 100%; max-width: 100%; }
  .row-cols-sm-2 > * { flex: 0 0 50%; max-width: 50%; }
  .row-cols-sm-3 > * { flex: 0 0 33.3333%; max-width: 33.3333%; }
  .row-cols-sm-4 > * { flex: 0 0 25%; max-width: 25%; }
  .row-cols-sm-5 > * { flex: 0 0 20%; max-width: 20%; }
  .row-cols-sm-6 > * { flex: 0 0 16.6667%; max-width: 16.6667%; }
  .col-sm-auto { flex: 0 0 auto; width: auto; max-width: 100%; }
  .col-sm-1 { flex: 0 0 8.33333%; max-width: 8.33333%; }
  .col-sm-2 { flex: 0 0 16.6667%; max-width: 16.6667%; }
  .col-sm-3 { flex: 0 0 25%; max-width: 25%; }
  .col-sm-4 { flex: 0 0 33.3333%; max-width: 33.3333%; }
  .col-sm-5 { flex: 0 0 41.6667%; max-width: 41.6667%; }
  .col-sm-6 { flex: 0 0 50%; max-width: 50%; }
  .col-sm-7 { flex: 0 0 58.3333%; max-width: 58.3333%; }
  .col-sm-8 { flex: 0 0 66.6667%; max-width: 66.6667%; }
  .col-sm-9 { flex: 0 0 75%; max-width: 75%; }
  .col-sm-10 { flex: 0 0 83.3333%; max-width: 83.3333%; }
  .col-sm-11 { flex: 0 0 91.6667%; max-width: 91.6667%; }
  .col-sm-12 { flex: 0 0 100%; max-width: 100%; }
  .order-sm-first { order: -1; }
  .order-sm-last { order: 13; }
  .order-sm-0 { order: 0; }
  .order-sm-1 { order: 1; }
  .order-sm-2 { order: 2; }
  .order-sm-3 { order: 3; }
  .order-sm-4 { order: 4; }
  .order-sm-5 { order: 5; }
  .order-sm-6 { order: 6; }
  .order-sm-7 { order: 7; }
  .order-sm-8 { order: 8; }
  .order-sm-9 { order: 9; }
  .order-sm-10 { order: 10; }
  .order-sm-11 { order: 11; }
  .order-sm-12 { order: 12; }
  .offset-sm-0 { margin-left: 0px; }
  .offset-sm-1 { margin-left: 8.33333%; }
  .offset-sm-2 { margin-left: 16.6667%; }
  .offset-sm-3 { margin-left: 25%; }
  .offset-sm-4 { margin-left: 33.3333%; }
  .offset-sm-5 { margin-left: 41.6667%; }
  .offset-sm-6 { margin-left: 50%; }
  .offset-sm-7 { margin-left: 58.3333%; }
  .offset-sm-8 { margin-left: 66.6667%; }
  .offset-sm-9 { margin-left: 75%; }
  .offset-sm-10 { margin-left: 83.3333%; }
  .offset-sm-11 { margin-left: 91.6667%; }
}
@media (min-width: 768px) {
  .col-md { flex-basis: 0px; flex-grow: 1; max-width: 100%; }
  .row-cols-md-1 > * { flex: 0 0 100%; max-width: 100%; }
  .row-cols-md-2 > * { flex: 0 0 50%; max-width: 50%; }
  .row-cols-md-3 > * { flex: 0 0 33.3333%; max-width: 33.3333%; }
  .row-cols-md-4 > * { flex: 0 0 25%; max-width: 25%; }
  .row-cols-md-5 > * { flex: 0 0 20%; max-width: 20%; }
  .row-cols-md-6 > * { flex: 0 0 16.6667%; max-width: 16.6667%; }
  .col-md-auto { flex: 0 0 auto; width: auto; max-width: 100%; }
  .col-md-1 { flex: 0 0 8.33333%; max-width: 8.33333%; }
  .col-md-2 { flex: 0 0 16.6667%; max-width: 16.6667%; }
  .col-md-3 { flex: 0 0 25%; max-width: 25%; }
  .col-md-4 { flex: 0 0 33.3333%; max-width: 33.3333%; }
  .col-md-5 { flex: 0 0 41.6667%; max-width: 41.6667%; }
  .col-md-6 { flex: 0 0 50%; max-width: 50%; }
  .col-md-7 { flex: 0 0 58.3333%; max-width: 58.3333%; }
  .col-md-8 { flex: 0 0 66.6667%; max-width: 66.6667%; }
  .col-md-9 { flex: 0 0 75%; max-width: 75%; }
  .col-md-10 { flex: 0 0 83.3333%; max-width: 83.3333%; }
  .col-md-11 { flex: 0 0 91.6667%; max-width: 91.6667%; }
  .col-md-12 { flex: 0 0 100%; max-width: 100%; }
  .order-md-first { order: -1; }
  .order-md-last { order: 13; }
  .order-md-0 { order: 0; }
  .order-md-1 { order: 1; }
  .order-md-2 { order: 2; }
  .order-md-3 { order: 3; }
  .order-md-4 { order: 4; }
  .order-md-5 { order: 5; }
  .order-md-6 { order: 6; }
  .order-md-7 { order: 7; }
  .order-md-8 { order: 8; }
  .order-md-9 { order: 9; }
  .order-md-10 { order: 10; }
  .order-md-11 { order: 11; }
  .order-md-12 { order: 12; }
  .offset-md-0 { margin-left: 0px; }
  .offset-md-1 { margin-left: 8.33333%; }
  .offset-md-2 { margin-left: 16.6667%; }
  .offset-md-3 { margin-left: 25%; }
  .offset-md-4 { margin-left: 33.3333%; }
  .offset-md-5 { margin-left: 41.6667%; }
  .offset-md-6 { margin-left: 50%; }
  .offset-md-7 { margin-left: 58.3333%; }
  .offset-md-8 { margin-left: 66.6667%; }
  .offset-md-9 { margin-left: 75%; }
  .offset-md-10 { margin-left: 83.3333%; }
  .offset-md-11 { margin-left: 91.6667%; }
}
@media (min-width: 992px) {
  .col-lg { flex-basis: 0px; flex-grow: 1; max-width: 100%; }
  .row-cols-lg-1 > * { flex: 0 0 100%; max-width: 100%; }
  .row-cols-lg-2 > * { flex: 0 0 50%; max-width: 50%; }
  .row-cols-lg-3 > * { flex: 0 0 33.3333%; max-width: 33.3333%; }
  .row-cols-lg-4 > * { flex: 0 0 25%; max-width: 25%; }
  .row-cols-lg-5 > * { flex: 0 0 20%; max-width: 20%; }
  .row-cols-lg-6 > * { flex: 0 0 16.6667%; max-width: 16.6667%; }
  .col-lg-auto { flex: 0 0 auto; width: auto; max-width: 100%; }
  .col-lg-1 { flex: 0 0 8.33333%; max-width: 8.33333%; }
  .col-lg-2 { flex: 0 0 16.6667%; max-width: 16.6667%; }
  .col-lg-3 { flex: 0 0 25%; max-width: 25%; }
  .col-lg-4 { flex: 0 0 33.3333%; max-width: 33.3333%; }
  .col-lg-5 { flex: 0 0 41.6667%; max-width: 41.6667%; }
  .col-lg-6 { flex: 0 0 50%; max-width: 50%; }
  .col-lg-7 { flex: 0 0 58.3333%; max-width: 58.3333%; }
  .col-lg-8 { flex: 0 0 66.6667%; max-width: 66.6667%; }
  .col-lg-9 { flex: 0 0 75%; max-width: 75%; }
  .col-lg-10 { flex: 0 0 83.3333%; max-width: 83.3333%; }
  .col-lg-11 { flex: 0 0 91.6667%; max-width: 91.6667%; }
  .col-lg-12 { flex: 0 0 100%; max-width: 100%; }
  .order-lg-first { order: -1; }
  .order-lg-last { order: 13; }
  .order-lg-0 { order: 0; }
  .order-lg-1 { order: 1; }
  .order-lg-2 { order: 2; }
  .order-lg-3 { order: 3; }
  .order-lg-4 { order: 4; }
  .order-lg-5 { order: 5; }
  .order-lg-6 { order: 6; }
  .order-lg-7 { order: 7; }
  .order-lg-8 { order: 8; }
  .order-lg-9 { order: 9; }
  .order-lg-10 { order: 10; }
  .order-lg-11 { order: 11; }
  .order-lg-12 { order: 12; }
  .offset-lg-0 { margin-left: 0px; }
  .offset-lg-1 { margin-left: 8.33333%; }
  .offset-lg-2 { margin-left: 16.6667%; }
  .offset-lg-3 { margin-left: 25%; }
  .offset-lg-4 { margin-left: 33.3333%; }
  .offset-lg-5 { margin-left: 41.6667%; }
  .offset-lg-6 { margin-left: 50%; }
  .offset-lg-7 { margin-left: 58.3333%; }
  .offset-lg-8 { margin-left: 66.6667%; }
  .offset-lg-9 { margin-left: 75%; }
  .offset-lg-10 { margin-left: 83.3333%; }
  .offset-lg-11 { margin-left: 91.6667%; }
}
@media (min-width: 1200px) {
  .col-xl { flex-basis: 0px; flex-grow: 1; max-width: 100%; }
  .row-cols-xl-1 > * { flex: 0 0 100%; max-width: 100%; }
  .row-cols-xl-2 > * { flex: 0 0 50%; max-width: 50%; }
  .row-cols-xl-3 > * { flex: 0 0 33.3333%; max-width: 33.3333%; }
  .row-cols-xl-4 > * { flex: 0 0 25%; max-width: 25%; }
  .row-cols-xl-5 > * { flex: 0 0 20%; max-width: 20%; }
  .row-cols-xl-6 > * { flex: 0 0 16.6667%; max-width: 16.6667%; }
  .col-xl-auto { flex: 0 0 auto; width: auto; max-width: 100%; }
  .col-xl-1 { flex: 0 0 8.33333%; max-width: 8.33333%; }
  .col-xl-2 { flex: 0 0 16.6667%; max-width: 16.6667%; }
  .col-xl-3 { flex: 0 0 25%; max-width: 25%; }
  .col-xl-4 { flex: 0 0 33.3333%; max-width: 33.3333%; }
  .col-xl-5 { flex: 0 0 41.6667%; max-width: 41.6667%; }
  .col-xl-6 { flex: 0 0 50%; max-width: 50%; }
  .col-xl-7 { flex: 0 0 58.3333%; max-width: 58.3333%; }
  .col-xl-8 { flex: 0 0 66.6667%; max-width: 66.6667%; }
  .col-xl-9 { flex: 0 0 75%; max-width: 75%; }
  .col-xl-10 { flex: 0 0 83.3333%; max-width: 83.3333%; }
  .col-xl-11 { flex: 0 0 91.6667%; max-width: 91.6667%; }
  .col-xl-12 { flex: 0 0 100%; max-width: 100%; }
  .order-xl-first { order: -1; }
  .order-xl-last { order: 13; }
  .order-xl-0 { order: 0; }
  .order-xl-1 { order: 1; }
  .order-xl-2 { order: 2; }
  .order-xl-3 { order: 3; }
  .order-xl-4 { order: 4; }
  .order-xl-5 { order: 5; }
  .order-xl-6 { order: 6; }
  .order-xl-7 { order: 7; }
  .order-xl-8 { order: 8; }
  .order-xl-9 { order: 9; }
  .order-xl-10 { order: 10; }
  .order-xl-11 { order: 11; }
  .order-xl-12 { order: 12; }
  .offset-xl-0 { margin-left: 0px; }
  .offset-xl-1 { margin-left: 8.33333%; }
  .offset-xl-2 { margin-left: 16.6667%; }
  .offset-xl-3 { margin-left: 25%; }
  .offset-xl-4 { margin-left: 33.3333%; }
  .offset-xl-5 { margin-left: 41.6667%; }
  .offset-xl-6 { margin-left: 50%; }
  .offset-xl-7 { margin-left: 58.3333%; }
  .offset-xl-8 { margin-left: 66.6667%; }
  .offset-xl-9 { margin-left: 75%; }
  .offset-xl-10 { margin-left: 83.3333%; }
  .offset-xl-11 { margin-left: 91.6667%; }
}
.table { width: 100%; margin-bottom: 1rem; color: rgb(133, 135, 150); }
.table td, .table th { padding: 0.75rem; vertical-align: top; border-top: 1px solid rgb(227, 230, 240); }
.table thead th { vertical-align: bottom; border-bottom: 2px solid rgb(227, 230, 240); }
.table tbody + tbody { border-top: 2px solid rgb(227, 230, 240); }
.table-sm td, .table-sm th { padding: 0.3rem; }
.table-bordered { border: 1px solid rgb(227, 230, 240); }
.table-bordered td, .table-bordered th { border: 1px solid rgb(227, 230, 240); }
.table-bordered thead td, .table-bordered thead th { border-bottom-width: 2px; }
.table-borderless tbody + tbody, .table-borderless td, .table-borderless th, .table-borderless thead th { border: 0px; }
.table-striped tbody tr:nth-of-type(2n+1) { background-color: rgba(0, 0, 0, 0.05); }
.table-hover tbody tr:hover { color: rgb(133, 135, 150); background-color: rgba(0, 0, 0, 0.075); }
.table-primary, .table-primary > td, .table-primary > th { background-color: rgb(205, 216, 246); }
.table-primary tbody + tbody, .table-primary td, .table-primary th, .table-primary thead th { border-color: rgb(163, 182, 238); }
.table-hover .table-primary:hover { background-color: rgb(183, 199, 242); }
.table-hover .table-primary:hover > td, .table-hover .table-primary:hover > th { background-color: rgb(183, 199, 242); }
.table-secondary, .table-secondary > td, .table-secondary > th { background-color: rgb(221, 221, 226); }
.table-secondary tbody + tbody, .table-secondary td, .table-secondary th, .table-secondary thead th { border-color: rgb(192, 193, 200); }
.table-hover .table-secondary:hover { background-color: rgb(207, 207, 214); }
.table-hover .table-secondary:hover > td, .table-hover .table-secondary:hover > th { background-color: rgb(207, 207, 214); }
.table-success, .table-success > td, .table-success > th { background-color: rgb(191, 240, 222); }
.table-success tbody + tbody, .table-success td, .table-success th, .table-success thead th { border-color: rgb(137, 226, 194); }
.table-hover .table-success:hover { background-color: rgb(170, 235, 211); }
.table-hover .table-success:hover > td, .table-hover .table-success:hover > th { background-color: rgb(170, 235, 211); }
.table-info, .table-info > td, .table-info > th { background-color: rgb(199, 235, 241); }
.table-info tbody + tbody, .table-info td, .table-info th, .table-info thead th { border-color: rgb(150, 219, 228); }
.table-hover .table-info:hover { background-color: rgb(179, 228, 236); }
.table-hover .table-info:hover > td, .table-hover .table-info:hover > th { background-color: rgb(179, 228, 236); }
.table-warning, .table-warning > td, .table-warning > th { background-color: rgb(252, 238, 201); }
.table-warning tbody + tbody, .table-warning td, .table-warning th, .table-warning thead th { border-color: rgb(250, 223, 155); }
.table-hover .table-warning:hover { background-color: rgb(251, 230, 177); }
.table-hover .table-warning:hover > td, .table-hover .table-warning:hover > th { background-color: rgb(251, 230, 177); }
.table-danger, .table-danger > td, .table-danger > th { background-color: rgb(248, 204, 200); }
.table-danger tbody + tbody, .table-danger td, .table-danger th, .table-danger thead th { border-color: rgb(243, 161, 153); }
.table-hover .table-danger:hover { background-color: rgb(245, 183, 177); }
.table-hover .table-danger:hover > td, .table-hover .table-danger:hover > th { background-color: rgb(245, 183, 177); }
.table-light, .table-light > td, .table-light > th { background-color: rgb(253, 253, 254); }
.table-light tbody + tbody, .table-light td, .table-light th, .table-light thead th { border-color: rgb(251, 252, 253); }
.table-hover .table-light:hover { background-color: rgb(236, 236, 246); }
.table-hover .table-light:hover > td, .table-hover .table-light:hover > th { background-color: rgb(236, 236, 246); }
.table-dark, .table-dark > td, .table-dark > th { background-color: rgb(209, 209, 213); }
.table-dark tbody + tbody, .table-dark td, .table-dark th, .table-dark thead th { border-color: rgb(169, 170, 177); }
.table-hover .table-dark:hover { background-color: rgb(196, 196, 201); }
.table-hover .table-dark:hover > td, .table-hover .table-dark:hover > th { background-color: rgb(196, 196, 201); }
.table-active, .table-active > td, .table-active > th { background-color: rgba(0, 0, 0, 0.075); }
.table-hover .table-active:hover { background-color: rgba(0, 0, 0, 0.075); }
.table-hover .table-active:hover > td, .table-hover .table-active:hover > th { background-color: rgba(0, 0, 0, 0.075); }
.table .thead-dark th { color: rgb(255, 255, 255); background-color: rgb(90, 92, 105); border-color: rgb(108, 110, 126); }
.table .thead-light th { color: rgb(110, 112, 126); background-color: rgb(234, 236, 244); border-color: rgb(227, 230, 240); }
.table-dark { color: rgb(255, 255, 255); background-color: rgb(90, 92, 105); }
.table-dark td, .table-dark th, .table-dark thead th { border-color: rgb(108, 110, 126); }
.table-dark.table-bordered { border: 0px; }
.table-dark.table-striped tbody tr:nth-of-type(2n+1) { background-color: rgba(255, 255, 255, 0.05); }
.table-dark.table-hover tbody tr:hover { color: rgb(255, 255, 255); background-color: rgba(255, 255, 255, 0.075); }
@media (max-width: 575.98px) {
  .table-responsive-sm { display: block; width: 100%; overflow-x: auto; }
  .table-responsive-sm > .table-bordered { border: 0px; }
}
@media (max-width: 767.98px) {
  .table-responsive-md { display: block; width: 100%; overflow-x: auto; }
  .table-responsive-md > .table-bordered { border: 0px; }
}
@media (max-width: 991.98px) {
  .table-responsive-lg { display: block; width: 100%; overflow-x: auto; }
  .table-responsive-lg > .table-bordered { border: 0px; }
}
@media (max-width: 1199.98px) {
  .table-responsive-xl { display: block; width: 100%; overflow-x: auto; }
  .table-responsive-xl > .table-bordered { border: 0px; }
}
.table-responsive { display: block; width: 100%; overflow-x: auto; }
.table-responsive > .table-bordered { border: 0px; }
.form-control { display: block; width: 100%; height: calc(1.5em + 0.75rem + 2px); padding: 0.375rem 0.75rem; font-size: 1rem; font-weight: 400; line-height: 1.5; color: rgb(110, 112, 126); background-color: rgb(255, 255, 255); background-clip: padding-box; border: 1px solid rgb(209, 211, 226); border-radius: 0.35rem; transition: border-color 0.15s ease-in-out 0s, box-shadow 0.15s ease-in-out 0s; }
@media (prefers-reduced-motion: reduce) {
  .form-control { transition: none 0s ease 0s; }
}
.form-control:focus { color: rgb(110, 112, 126); background-color: rgb(255, 255, 255); border-color: rgb(186, 200, 243); outline: 0px; box-shadow: rgba(78, 115, 223, 0.25) 0px 0px 0px 0.2rem; }
.form-control::-webkit-input-placeholder { color: rgb(133, 135, 150); opacity: 1; }
.form-control::placeholder { color: rgb(133, 135, 150); opacity: 1; }
.form-control:disabled, .form-control[readonly] { background-color: rgb(234, 236, 244); opacity: 1; }
input[type="date"].form-control, input[type="datetime-local"].form-control, input[type="month"].form-control, input[type="time"].form-control { appearance: none; }
.form-control-file, .form-control-range { display: block; width: 100%; }
.col-form-label { padding-top: calc(0.375rem + 1px); padding-bottom: calc(0.375rem + 1px); margin-bottom: 0px; font-size: inherit; line-height: 1.5; }
.col-form-label-lg { padding-top: calc(0.5rem + 1px); padding-bottom: calc(0.5rem + 1px); font-size: 1.25rem; line-height: 1.5; }
.col-form-label-sm { padding-top: calc(0.25rem + 1px); padding-bottom: calc(0.25rem + 1px); font-size: 0.875rem; line-height: 1.5; }
.form-control-plaintext { display: block; width: 100%; padding: 0.375rem 0px; margin-bottom: 0px; font-size: 1rem; line-height: 1.5; color: rgb(133, 135, 150); background-color: transparent; border-style: solid; border-color: transparent; border-image: initial; border-width: 1px 0px; }
.form-control-plaintext.form-control-lg, .form-control-plaintext.form-control-sm { padding-right: 0px; padding-left: 0px; }
.form-control-sm { height: calc(1.5em + 0.5rem + 2px); padding: 0.25rem 0.5rem; font-size: 0.875rem; line-height: 1.5; border-radius: 0.2rem; }
.form-control-lg { height: calc(1.5em + 1rem + 2px); padding: 0.5rem 1rem; font-size: 1.25rem; line-height: 1.5; border-radius: 0.3rem; }
select.form-control[multiple], select.form-control[size] { height: auto; }
textarea.form-control { height: auto; }
.form-group { margin-bottom: 1rem; }
.form-text { display: block; margin-top: 0.25rem; }
.form-row { display: flex; flex-wrap: wrap; margin-right: -5px; margin-left: -5px; }
.form-row > .col, .form-row > [class*="col-"] { padding-right: 5px; padding-left: 5px; }
.form-check { position: relative; display: block; padding-left: 1.25rem; }
.form-check-input { position: absolute; margin-top: 0.3rem; margin-left: -1.25rem; }
.form-check-input:disabled ~ .form-check-label, .form-check-input[disabled] ~ .form-check-label { color: rgb(133, 135, 150); }
.form-check-label { margin-bottom: 0px; }
.form-check-inline { display: inline-flex; align-items: center; padding-left: 0px; margin-right: 0.75rem; }
.form-check-inline .form-check-input { position: static; margin-top: 0px; margin-right: 0.3125rem; margin-left: 0px; }
.valid-feedback { display: none; width: 100%; margin-top: 0.25rem; font-size: 80%; color: rgb(28, 200, 138); }
.valid-tooltip { position: absolute; top: 100%; left: 0px; z-index: 5; display: none; max-width: 100%; padding: 0.25rem 0.5rem; margin-top: 0.1rem; font-size: 0.875rem; line-height: 1.5; color: rgb(255, 255, 255); background-color: rgba(28, 200, 138, 0.9); border-radius: 0.35rem; }
.form-row > .col > .valid-tooltip, .form-row > [class*="col-"] > .valid-tooltip { left: 5px; }
.is-valid ~ .valid-feedback, .is-valid ~ .valid-tooltip, .was-validated :valid ~ .valid-feedback, .was-validated :valid ~ .valid-tooltip { display: block; }
.form-control.is-valid, .was-validated .form-control:valid { border-color: rgb(28, 200, 138); padding-right: calc(1.5em + 0.75rem); background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='8' height='8' viewBox='0 0 8 8'%3e%3cpath fill='%231cc88a' d='M2.3 6.73L.6 4.53c-.4-1.04.46-1.4 1.1-.8l1.1 1.4 3.4-3.8c.6-.63 1.6-.27 1.2.7l-4 4.6c-.43.5-.8.4-1.1.1z'/%3e%3c/svg%3e"); background-repeat: no-repeat; background-position: right calc(0.375em + 0.1875rem) center; background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem); }
.form-control.is-valid:focus, .was-validated .form-control:valid:focus { border-color: rgb(28, 200, 138); box-shadow: rgba(28, 200, 138, 0.25) 0px 0px 0px 0.2rem; }
.was-validated textarea.form-control:valid, textarea.form-control.is-valid { padding-right: calc(1.5em + 0.75rem); background-position: right calc(0.375em + 0.1875rem) top calc(0.375em + 0.1875rem); }
.custom-select.is-valid, .was-validated .custom-select:valid { border-color: rgb(28, 200, 138); padding-right: calc(0.75em + 2.3125rem); background: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='4' height='5' viewBox='0 0 4 5'%3e%3cpath fill='%235a5c69' d='M2 0L0 2h4zm0 5L0 3h4z'/%3e%3c/svg%3e") right 0.75rem center / 8px 10px no-repeat, url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='8' height='8' viewBox='0 0 8 8'%3e%3cpath fill='%231cc88a' d='M2.3 6.73L.6 4.53c-.4-1.04.46-1.4 1.1-.8l1.1 1.4 3.4-3.8c.6-.63 1.6-.27 1.2.7l-4 4.6c-.43.5-.8.4-1.1.1z'/%3e%3c/svg%3e") right 1.75rem center / calc(0.75em + 0.375rem) calc(0.75em + 0.375rem) no-repeat rgb(255, 255, 255); }
.custom-select.is-valid:focus, .was-validated .custom-select:valid:focus { border-color: rgb(28, 200, 138); box-shadow: rgba(28, 200, 138, 0.25) 0px 0px 0px 0.2rem; }
.form-check-input.is-valid ~ .form-check-label, .was-validated .form-check-input:valid ~ .form-check-label { color: rgb(28, 200, 138); }
.form-check-input.is-valid ~ .valid-feedback, .form-check-input.is-valid ~ .valid-tooltip, .was-validated .form-check-input:valid ~ .valid-feedback, .was-validated .form-check-input:valid ~ .valid-tooltip { display: block; }
.custom-control-input.is-valid ~ .custom-control-label, .was-validated .custom-control-input:valid ~ .custom-control-label { color: rgb(28, 200, 138); }
.custom-control-input.is-valid ~ .custom-control-label::before, .was-validated .custom-control-input:valid ~ .custom-control-label::before { border-color: rgb(28, 200, 138); }
.custom-control-input.is-valid:checked ~ .custom-control-label::before, .was-validated .custom-control-input:valid:checked ~ .custom-control-label::before { border-color: rgb(52, 227, 164); background-color: rgb(52, 227, 164); }
.custom-control-input.is-valid:focus ~ .custom-control-label::before, .was-validated .custom-control-input:valid:focus ~ .custom-control-label::before { box-shadow: rgba(28, 200, 138, 0.25) 0px 0px 0px 0.2rem; }
.custom-control-input.is-valid:focus:not(:checked) ~ .custom-control-label::before, .was-validated .custom-control-input:valid:focus:not(:checked) ~ .custom-control-label::before { border-color: rgb(28, 200, 138); }
.custom-file-input.is-valid ~ .custom-file-label, .was-validated .custom-file-input:valid ~ .custom-file-label { border-color: rgb(28, 200, 138); }
.custom-file-input.is-valid:focus ~ .custom-file-label, .was-validated .custom-file-input:valid:focus ~ .custom-file-label { border-color: rgb(28, 200, 138); box-shadow: rgba(28, 200, 138, 0.25) 0px 0px 0px 0.2rem; }
.invalid-feedback { display: none; width: 100%; margin-top: 0.25rem; font-size: 80%; color: rgb(231, 74, 59); }
.invalid-tooltip { position: absolute; top: 100%; left: 0px; z-index: 5; display: none; max-width: 100%; padding: 0.25rem 0.5rem; margin-top: 0.1rem; font-size: 0.875rem; line-height: 1.5; color: rgb(255, 255, 255); background-color: rgba(231, 74, 59, 0.9); border-radius: 0.35rem; }
.form-row > .col > .invalid-tooltip, .form-row > [class*="col-"] > .invalid-tooltip { left: 5px; }
.is-invalid ~ .invalid-feedback, .is-invalid ~ .invalid-tooltip, .was-validated :invalid ~ .invalid-feedback, .was-validated :invalid ~ .invalid-tooltip { display: block; }
.form-control.is-invalid, .was-validated .form-control:invalid { border-color: rgb(231, 74, 59); padding-right: calc(1.5em + 0.75rem); background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='none' stroke='%23e74a3b' viewBox='0 0 12 12'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23e74a3b' stroke='none'/%3e%3c/svg%3e"); background-repeat: no-repeat; background-position: right calc(0.375em + 0.1875rem) center; background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem); }
.form-control.is-invalid:focus, .was-validated .form-control:invalid:focus { border-color: rgb(231, 74, 59); box-shadow: rgba(231, 74, 59, 0.25) 0px 0px 0px 0.2rem; }
.was-validated textarea.form-control:invalid, textarea.form-control.is-invalid { padding-right: calc(1.5em + 0.75rem); background-position: right calc(0.375em + 0.1875rem) top calc(0.375em + 0.1875rem); }
.custom-select.is-invalid, .was-validated .custom-select:invalid { border-color: rgb(231, 74, 59); padding-right: calc(0.75em + 2.3125rem); background: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='4' height='5' viewBox='0 0 4 5'%3e%3cpath fill='%235a5c69' d='M2 0L0 2h4zm0 5L0 3h4z'/%3e%3c/svg%3e") right 0.75rem center / 8px 10px no-repeat, url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='none' stroke='%23e74a3b' viewBox='0 0 12 12'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23e74a3b' stroke='none'/%3e%3c/svg%3e") right 1.75rem center / calc(0.75em + 0.375rem) calc(0.75em + 0.375rem) no-repeat rgb(255, 255, 255); }
.custom-select.is-invalid:focus, .was-validated .custom-select:invalid:focus { border-color: rgb(231, 74, 59); box-shadow: rgba(231, 74, 59, 0.25) 0px 0px 0px 0.2rem; }
.form-check-input.is-invalid ~ .form-check-label, .was-validated .form-check-input:invalid ~ .form-check-label { color: rgb(231, 74, 59); }
.form-check-input.is-invalid ~ .invalid-feedback, .form-check-input.is-invalid ~ .invalid-tooltip, .was-validated .form-check-input:invalid ~ .invalid-feedback, .was-validated .form-check-input:invalid ~ .invalid-tooltip { display: block; }
.custom-control-input.is-invalid ~ .custom-control-label, .was-validated .custom-control-input:invalid ~ .custom-control-label { color: rgb(231, 74, 59); }
.custom-control-input.is-invalid ~ .custom-control-label::before, .was-validated .custom-control-input:invalid ~ .custom-control-label::before { border-color: rgb(231, 74, 59); }
.custom-control-input.is-invalid:checked ~ .custom-control-label::before, .was-validated .custom-control-input:invalid:checked ~ .custom-control-label::before { border-color: rgb(237, 116, 104); background-color: rgb(237, 116, 104); }
.custom-control-input.is-invalid:focus ~ .custom-control-label::before, .was-validated .custom-control-input:invalid:focus ~ .custom-control-label::before { box-shadow: rgba(231, 74, 59, 0.25) 0px 0px 0px 0.2rem; }
.custom-control-input.is-invalid:focus:not(:checked) ~ .custom-control-label::before, .was-validated .custom-control-input:invalid:focus:not(:checked) ~ .custom-control-label::before { border-color: rgb(231, 74, 59); }
.custom-file-input.is-invalid ~ .custom-file-label, .was-validated .custom-file-input:invalid ~ .custom-file-label { border-color: rgb(231, 74, 59); }
.custom-file-input.is-invalid:focus ~ .custom-file-label, .was-validated .custom-file-input:invalid:focus ~ .custom-file-label { border-color: rgb(231, 74, 59); box-shadow: rgba(231, 74, 59, 0.25) 0px 0px 0px 0.2rem; }
.form-inline { display: flex; flex-flow: wrap; align-items: center; }
.form-inline .form-check { width: 100%; }
@media (min-width: 576px) {
  .form-inline label { display: flex; align-items: center; justify-content: center; margin-bottom: 0px; }
  .form-inline .form-group { display: flex; flex: 0 0 auto; flex-flow: wrap; align-items: center; margin-bottom: 0px; }
  .form-inline .form-control { display: inline-block; width: auto; vertical-align: middle; }
  .form-inline .form-control-plaintext { display: inline-block; }
  .form-inline .custom-select, .form-inline .input-group { width: auto; }
  .form-inline .form-check { display: flex; align-items: center; justify-content: center; width: auto; padding-left: 0px; }
  .form-inline .form-check-input { position: relative; flex-shrink: 0; margin-top: 0px; margin-right: 0.25rem; margin-left: 0px; }
  .form-inline .custom-control { align-items: center; justify-content: center; }
  .form-inline .custom-control-label { margin-bottom: 0px; }
}
.btn { display: inline-block; font-weight: 400; color: rgb(133, 135, 150); text-align: center; vertical-align: middle; user-select: none; background-color: transparent; border: 1px solid transparent; padding: 0.375rem 0.75rem; font-size: 1rem; line-height: 1.5; border-radius: 0.35rem; transition: color 0.15s ease-in-out 0s, background-color 0.15s ease-in-out 0s, border-color 0.15s ease-in-out 0s, box-shadow 0.15s ease-in-out 0s; }
@media (prefers-reduced-motion: reduce) {
  .btn { transition: none 0s ease 0s; }
}
.btn:hover { color: rgb(133, 135, 150); text-decoration: none; }
.btn.focus, .btn:focus { outline: 0px; box-shadow: rgba(78, 115, 223, 0.25) 0px 0px 0px 0.2rem; }
.btn.disabled, .btn:disabled { opacity: 0.65; }
.btn:not(:disabled):not(.disabled) { cursor: pointer; }
a.btn.disabled, fieldset:disabled a.btn { pointer-events: none; }
.btn-primary { color: rgb(255, 255, 255); background-color: rgb(78, 115, 223); border-color: rgb(78, 115, 223); }
.btn-primary:hover { color: rgb(255, 255, 255); background-color: rgb(46, 89, 217); border-color: rgb(38, 83, 212); }
.btn-primary.focus, .btn-primary:focus { color: rgb(255, 255, 255); background-color: rgb(46, 89, 217); border-color: rgb(38, 83, 212); box-shadow: rgba(105, 136, 228, 0.5) 0px 0px 0px 0.2rem; }
.btn-primary.disabled, .btn-primary:disabled { color: rgb(255, 255, 255); background-color: rgb(78, 115, 223); border-color: rgb(78, 115, 223); }
.btn-primary:not(:disabled):not(.disabled).active, .btn-primary:not(:disabled):not(.disabled):active, .show > .btn-primary.dropdown-toggle { color: rgb(255, 255, 255); background-color: rgb(38, 83, 212); border-color: rgb(36, 78, 201); }
.btn-primary:not(:disabled):not(.disabled).active:focus, .btn-primary:not(:disabled):not(.disabled):active:focus, .show > .btn-primary.dropdown-toggle:focus { box-shadow: rgba(105, 136, 228, 0.5) 0px 0px 0px 0.2rem; }
.btn-secondary { color: rgb(255, 255, 255); background-color: rgb(133, 135, 150); border-color: rgb(133, 135, 150); }
.btn-secondary:hover { color: rgb(255, 255, 255); background-color: rgb(113, 115, 132); border-color: rgb(107, 109, 125); }
.btn-secondary.focus, .btn-secondary:focus { color: rgb(255, 255, 255); background-color: rgb(113, 115, 132); border-color: rgb(107, 109, 125); box-shadow: rgba(151, 153, 166, 0.5) 0px 0px 0px 0.2rem; }
.btn-secondary.disabled, .btn-secondary:disabled { color: rgb(255, 255, 255); background-color: rgb(133, 135, 150); border-color: rgb(133, 135, 150); }
.btn-secondary:not(:disabled):not(.disabled).active, .btn-secondary:not(:disabled):not(.disabled):active, .show > .btn-secondary.dropdown-toggle { color: rgb(255, 255, 255); background-color: rgb(107, 109, 125); border-color: rgb(101, 103, 118); }
.btn-secondary:not(:disabled):not(.disabled).active:focus, .btn-secondary:not(:disabled):not(.disabled):active:focus, .show > .btn-secondary.dropdown-toggle:focus { box-shadow: rgba(151, 153, 166, 0.5) 0px 0px 0px 0.2rem; }
.btn-success { color: rgb(255, 255, 255); background-color: rgb(28, 200, 138); border-color: rgb(28, 200, 138); }
.btn-success:hover { color: rgb(255, 255, 255); background-color: rgb(23, 166, 115); border-color: rgb(22, 155, 107); }
.btn-success.focus, .btn-success:focus { color: rgb(255, 255, 255); background-color: rgb(23, 166, 115); border-color: rgb(22, 155, 107); box-shadow: rgba(62, 208, 156, 0.5) 0px 0px 0px 0.2rem; }
.btn-success.disabled, .btn-success:disabled { color: rgb(255, 255, 255); background-color: rgb(28, 200, 138); border-color: rgb(28, 200, 138); }
.btn-success:not(:disabled):not(.disabled).active, .btn-success:not(:disabled):not(.disabled):active, .show > .btn-success.dropdown-toggle { color: rgb(255, 255, 255); background-color: rgb(22, 155, 107); border-color: rgb(20, 144, 99); }
.btn-success:not(:disabled):not(.disabled).active:focus, .btn-success:not(:disabled):not(.disabled):active:focus, .show > .btn-success.dropdown-toggle:focus { box-shadow: rgba(62, 208, 156, 0.5) 0px 0px 0px 0.2rem; }
.btn-info { color: rgb(255, 255, 255); background-color: rgb(54, 185, 204); border-color: rgb(54, 185, 204); }
.btn-info:hover { color: rgb(255, 255, 255); background-color: rgb(44, 159, 175); border-color: rgb(42, 150, 165); }
.btn-info.focus, .btn-info:focus { color: rgb(255, 255, 255); background-color: rgb(44, 159, 175); border-color: rgb(42, 150, 165); box-shadow: rgba(84, 196, 212, 0.5) 0px 0px 0px 0.2rem; }
.btn-info.disabled, .btn-info:disabled { color: rgb(255, 255, 255); background-color: rgb(54, 185, 204); border-color: rgb(54, 185, 204); }
.btn-info:not(:disabled):not(.disabled).active, .btn-info:not(:disabled):not(.disabled):active, .show > .btn-info.dropdown-toggle { color: rgb(255, 255, 255); background-color: rgb(42, 150, 165); border-color: rgb(39, 140, 155); }
.btn-info:not(:disabled):not(.disabled).active:focus, .btn-info:not(:disabled):not(.disabled):active:focus, .show > .btn-info.dropdown-toggle:focus { box-shadow: rgba(84, 196, 212, 0.5) 0px 0px 0px 0.2rem; }
.btn-warning { color: rgb(255, 255, 255); background-color: rgb(246, 194, 62); border-color: rgb(246, 194, 62); }
.btn-warning:hover { color: rgb(255, 255, 255); background-color: rgb(244, 182, 25); border-color: rgb(244, 179, 13); }
.btn-warning.focus, .btn-warning:focus { color: rgb(255, 255, 255); background-color: rgb(244, 182, 25); border-color: rgb(244, 179, 13); box-shadow: rgba(247, 203, 91, 0.5) 0px 0px 0px 0.2rem; }
.btn-warning.disabled, .btn-warning:disabled { color: rgb(255, 255, 255); background-color: rgb(246, 194, 62); border-color: rgb(246, 194, 62); }
.btn-warning:not(:disabled):not(.disabled).active, .btn-warning:not(:disabled):not(.disabled):active, .show > .btn-warning.dropdown-toggle { color: rgb(255, 255, 255); background-color: rgb(244, 179, 13); border-color: rgb(233, 170, 11); }
.btn-warning:not(:disabled):not(.disabled).active:focus, .btn-warning:not(:disabled):not(.disabled):active:focus, .show > .btn-warning.dropdown-toggle:focus { box-shadow: rgba(247, 203, 91, 0.5) 0px 0px 0px 0.2rem; }
.btn-danger { color: rgb(255, 255, 255); background-color: rgb(231, 74, 59); border-color: rgb(231, 74, 59); }
.btn-danger:hover { color: rgb(255, 255, 255); background-color: rgb(224, 45, 27); border-color: rgb(213, 42, 26); }
.btn-danger.focus, .btn-danger:focus { color: rgb(255, 255, 255); background-color: rgb(224, 45, 27); border-color: rgb(213, 42, 26); box-shadow: rgba(235, 101, 88, 0.5) 0px 0px 0px 0.2rem; }
.btn-danger.disabled, .btn-danger:disabled { color: rgb(255, 255, 255); background-color: rgb(231, 74, 59); border-color: rgb(231, 74, 59); }
.btn-danger:not(:disabled):not(.disabled).active, .btn-danger:not(:disabled):not(.disabled):active, .show > .btn-danger.dropdown-toggle { color: rgb(255, 255, 255); background-color: rgb(213, 42, 26); border-color: rgb(202, 40, 25); }
.btn-danger:not(:disabled):not(.disabled).active:focus, .btn-danger:not(:disabled):not(.disabled):active:focus, .show > .btn-danger.dropdown-toggle:focus { box-shadow: rgba(235, 101, 88, 0.5) 0px 0px 0px 0.2rem; }
.btn-light { color: rgb(58, 59, 69); background-color: rgb(248, 249, 252); border-color: rgb(248, 249, 252); }
.btn-light:hover { color: rgb(58, 59, 69); background-color: rgb(221, 226, 241); border-color: rgb(212, 218, 237); }
.btn-light.focus, .btn-light:focus { color: rgb(58, 59, 69); background-color: rgb(221, 226, 241); border-color: rgb(212, 218, 237); box-shadow: rgba(220, 221, 225, 0.5) 0px 0px 0px 0.2rem; }
.btn-light.disabled, .btn-light:disabled { color: rgb(58, 59, 69); background-color: rgb(248, 249, 252); border-color: rgb(248, 249, 252); }
.btn-light:not(:disabled):not(.disabled).active, .btn-light:not(:disabled):not(.disabled):active, .show > .btn-light.dropdown-toggle { color: rgb(58, 59, 69); background-color: rgb(212, 218, 237); border-color: rgb(203, 211, 233); }
.btn-light:not(:disabled):not(.disabled).active:focus, .btn-light:not(:disabled):not(.disabled):active:focus, .show > .btn-light.dropdown-toggle:focus { box-shadow: rgba(220, 221, 225, 0.5) 0px 0px 0px 0.2rem; }
.btn-dark { color: rgb(255, 255, 255); background-color: rgb(90, 92, 105); border-color: rgb(90, 92, 105); }
.btn-dark:hover { color: rgb(255, 255, 255); background-color: rgb(72, 74, 84); border-color: rgb(66, 68, 78); }
.btn-dark.focus, .btn-dark:focus { color: rgb(255, 255, 255); background-color: rgb(72, 74, 84); border-color: rgb(66, 68, 78); box-shadow: rgba(115, 116, 128, 0.5) 0px 0px 0px 0.2rem; }
.btn-dark.disabled, .btn-dark:disabled { color: rgb(255, 255, 255); background-color: rgb(90, 92, 105); border-color: rgb(90, 92, 105); }
.btn-dark:not(:disabled):not(.disabled).active, .btn-dark:not(:disabled):not(.disabled):active, .show > .btn-dark.dropdown-toggle { color: rgb(255, 255, 255); background-color: rgb(66, 68, 78); border-color: rgb(61, 62, 71); }
.btn-dark:not(:disabled):not(.disabled).active:focus, .btn-dark:not(:disabled):not(.disabled):active:focus, .show > .btn-dark.dropdown-toggle:focus { box-shadow: rgba(115, 116, 128, 0.5) 0px 0px 0px 0.2rem; }
.btn-outline-primary { color: rgb(78, 115, 223); border-color: rgb(78, 115, 223); }
.btn-outline-primary:hover { color: rgb(255, 255, 255); background-color: rgb(78, 115, 223); border-color: rgb(78, 115, 223); }
.btn-outline-primary.focus, .btn-outline-primary:focus { box-shadow: rgba(78, 115, 223, 0.5) 0px 0px 0px 0.2rem; }
.btn-outline-primary.disabled, .btn-outline-primary:disabled { color: rgb(78, 115, 223); background-color: transparent; }
.btn-outline-primary:not(:disabled):not(.disabled).active, .btn-outline-primary:not(:disabled):not(.disabled):active, .show > .btn-outline-primary.dropdown-toggle { color: rgb(255, 255, 255); background-color: rgb(78, 115, 223); border-color: rgb(78, 115, 223); }
.btn-outline-primary:not(:disabled):not(.disabled).active:focus, .btn-outline-primary:not(:disabled):not(.disabled):active:focus, .show > .btn-outline-primary.dropdown-toggle:focus { box-shadow: rgba(78, 115, 223, 0.5) 0px 0px 0px 0.2rem; }
.btn-outline-secondary { color: rgb(133, 135, 150); border-color: rgb(133, 135, 150); }
.btn-outline-secondary:hover { color: rgb(255, 255, 255); background-color: rgb(133, 135, 150); border-color: rgb(133, 135, 150); }
.btn-outline-secondary.focus, .btn-outline-secondary:focus { box-shadow: rgba(133, 135, 150, 0.5) 0px 0px 0px 0.2rem; }
.btn-outline-secondary.disabled, .btn-outline-secondary:disabled { color: rgb(133, 135, 150); background-color: transparent; }
.btn-outline-secondary:not(:disabled):not(.disabled).active, .btn-outline-secondary:not(:disabled):not(.disabled):active, .show > .btn-outline-secondary.dropdown-toggle { color: rgb(255, 255, 255); background-color: rgb(133, 135, 150); border-color: rgb(133, 135, 150); }
.btn-outline-secondary:not(:disabled):not(.disabled).active:focus, .btn-outline-secondary:not(:disabled):not(.disabled):active:focus, .show > .btn-outline-secondary.dropdown-toggle:focus { box-shadow: rgba(133, 135, 150, 0.5) 0px 0px 0px 0.2rem; }
.btn-outline-success { color: rgb(28, 200, 138); border-color: rgb(28, 200, 138); }
.btn-outline-success:hover { color: rgb(255, 255, 255); background-color: rgb(28, 200, 138); border-color: rgb(28, 200, 138); }
.btn-outline-success.focus, .btn-outline-success:focus { box-shadow: rgba(28, 200, 138, 0.5) 0px 0px 0px 0.2rem; }
.btn-outline-success.disabled, .btn-outline-success:disabled { color: rgb(28, 200, 138); background-color: transparent; }
.btn-outline-success:not(:disabled):not(.disabled).active, .btn-outline-success:not(:disabled):not(.disabled):active, .show > .btn-outline-success.dropdown-toggle { color: rgb(255, 255, 255); background-color: rgb(28, 200, 138); border-color: rgb(28, 200, 138); }
.btn-outline-success:not(:disabled):not(.disabled).active:focus, .btn-outline-success:not(:disabled):not(.disabled):active:focus, .show > .btn-outline-success.dropdown-toggle:focus { box-shadow: rgba(28, 200, 138, 0.5) 0px 0px 0px 0.2rem; }
.btn-outline-info { color: rgb(54, 185, 204); border-color: rgb(54, 185, 204); }
.btn-outline-info:hover { color: rgb(255, 255, 255); background-color: rgb(54, 185, 204); border-color: rgb(54, 185, 204); }
.btn-outline-info.focus, .btn-outline-info:focus { box-shadow: rgba(54, 185, 204, 0.5) 0px 0px 0px 0.2rem; }
.btn-outline-info.disabled, .btn-outline-info:disabled { color: rgb(54, 185, 204); background-color: transparent; }
.btn-outline-info:not(:disabled):not(.disabled).active, .btn-outline-info:not(:disabled):not(.disabled):active, .show > .btn-outline-info.dropdown-toggle { color: rgb(255, 255, 255); background-color: rgb(54, 185, 204); border-color: rgb(54, 185, 204); }
.btn-outline-info:not(:disabled):not(.disabled).active:focus, .btn-outline-info:not(:disabled):not(.disabled):active:focus, .show > .btn-outline-info.dropdown-toggle:focus { box-shadow: rgba(54, 185, 204, 0.5) 0px 0px 0px 0.2rem; }
.btn-outline-warning { color: rgb(246, 194, 62); border-color: rgb(246, 194, 62); }
.btn-outline-warning:hover { color: rgb(255, 255, 255); background-color: rgb(246, 194, 62); border-color: rgb(246, 194, 62); }
.btn-outline-warning.focus, .btn-outline-warning:focus { box-shadow: rgba(246, 194, 62, 0.5) 0px 0px 0px 0.2rem; }
.btn-outline-warning.disabled, .btn-outline-warning:disabled { color: rgb(246, 194, 62); background-color: transparent; }
.btn-outline-warning:not(:disabled):not(.disabled).active, .btn-outline-warning:not(:disabled):not(.disabled):active, .show > .btn-outline-warning.dropdown-toggle { color: rgb(255, 255, 255); background-color: rgb(246, 194, 62); border-color: rgb(246, 194, 62); }
.btn-outline-warning:not(:disabled):not(.disabled).active:focus, .btn-outline-warning:not(:disabled):not(.disabled):active:focus, .show > .btn-outline-warning.dropdown-toggle:focus { box-shadow: rgba(246, 194, 62, 0.5) 0px 0px 0px 0.2rem; }
.btn-outline-danger { color: rgb(231, 74, 59); border-color: rgb(231, 74, 59); }
.btn-outline-danger:hover { color: rgb(255, 255, 255); background-color: rgb(231, 74, 59); border-color: rgb(231, 74, 59); }
.btn-outline-danger.focus, .btn-outline-danger:focus { box-shadow: rgba(231, 74, 59, 0.5) 0px 0px 0px 0.2rem; }
.btn-outline-danger.disabled, .btn-outline-danger:disabled { color: rgb(231, 74, 59); background-color: transparent; }
.btn-outline-danger:not(:disabled):not(.disabled).active, .btn-outline-danger:not(:disabled):not(.disabled):active, .show > .btn-outline-danger.dropdown-toggle { color: rgb(255, 255, 255); background-color: rgb(231, 74, 59); border-color: rgb(231, 74, 59); }
.btn-outline-danger:not(:disabled):not(.disabled).active:focus, .btn-outline-danger:not(:disabled):not(.disabled):active:focus, .show > .btn-outline-danger.dropdown-toggle:focus { box-shadow: rgba(231, 74, 59, 0.5) 0px 0px 0px 0.2rem; }
.btn-outline-light { color: rgb(248, 249, 252); border-color: rgb(248, 249, 252); }
.btn-outline-light:hover { color: rgb(58, 59, 69); background-color: rgb(248, 249, 252); border-color: rgb(248, 249, 252); }
.btn-outline-light.focus, .btn-outline-light:focus { box-shadow: rgba(248, 249, 252, 0.5) 0px 0px 0px 0.2rem; }
.btn-outline-light.disabled, .btn-outline-light:disabled { color: rgb(248, 249, 252); background-color: transparent; }
.btn-outline-light:not(:disabled):not(.disabled).active, .btn-outline-light:not(:disabled):not(.disabled):active, .show > .btn-outline-light.dropdown-toggle { color: rgb(58, 59, 69); background-color: rgb(248, 249, 252); border-color: rgb(248, 249, 252); }
.btn-outline-light:not(:disabled):not(.disabled).active:focus, .btn-outline-light:not(:disabled):not(.disabled):active:focus, .show > .btn-outline-light.dropdown-toggle:focus { box-shadow: rgba(248, 249, 252, 0.5) 0px 0px 0px 0.2rem; }
.btn-outline-dark { color: rgb(90, 92, 105); border-color: rgb(90, 92, 105); }
.btn-outline-dark:hover { color: rgb(255, 255, 255); background-color: rgb(90, 92, 105); border-color: rgb(90, 92, 105); }
.btn-outline-dark.focus, .btn-outline-dark:focus { box-shadow: rgba(90, 92, 105, 0.5) 0px 0px 0px 0.2rem; }
.btn-outline-dark.disabled, .btn-outline-dark:disabled { color: rgb(90, 92, 105); background-color: transparent; }
.btn-outline-dark:not(:disabled):not(.disabled).active, .btn-outline-dark:not(:disabled):not(.disabled):active, .show > .btn-outline-dark.dropdown-toggle { color: rgb(255, 255, 255); background-color: rgb(90, 92, 105); border-color: rgb(90, 92, 105); }
.btn-outline-dark:not(:disabled):not(.disabled).active:focus, .btn-outline-dark:not(:disabled):not(.disabled):active:focus, .show > .btn-outline-dark.dropdown-toggle:focus { box-shadow: rgba(90, 92, 105, 0.5) 0px 0px 0px 0.2rem; }
.btn-link { font-weight: 400; color: rgb(78, 115, 223); text-decoration: none; }
.btn-link:hover { color: rgb(34, 74, 190); text-decoration: underline; }
.btn-link.focus, .btn-link:focus { text-decoration: underline; }
.btn-link.disabled, .btn-link:disabled { color: rgb(133, 135, 150); pointer-events: none; }
.btn-group-lg > .btn, .btn-lg { padding: 0.5rem 1rem; font-size: 1.25rem; line-height: 1.5; border-radius: 0.3rem; }
.btn-group-sm > .btn, .btn-sm { padding: 0.25rem 0.5rem; font-size: 0.875rem; line-height: 1.5; border-radius: 0.2rem; }
.btn-block { display: block; width: 100%; }
.btn-block + .btn-block { margin-top: 0.5rem; }
input[type="button"].btn-block, input[type="reset"].btn-block, input[type="submit"].btn-block { width: 100%; }
.fade { transition: opacity 0.15s linear 0s; }
@media (prefers-reduced-motion: reduce) {
  .fade { transition: none 0s ease 0s; }
}
.fade:not(.show) { opacity: 0; }
.collapse:not(.show) { display: none; }
.collapsing { position: relative; height: 0px; overflow: hidden; transition: height 0.15s ease 0s; }
@media (prefers-reduced-motion: reduce) {
  .collapsing { transition: none 0s ease 0s; }
}
.dropdown, .dropleft, .dropright, .dropup { position: relative; }
.dropdown-toggle { white-space: nowrap; }
.dropdown-toggle::after { display: inline-block; margin-left: 0.255em; vertical-align: 0.255em; content: ""; border-width: 0.3em 0.3em 0px; border-top-style: solid; border-top-color: initial; border-right-style: solid; border-right-color: transparent; border-bottom-style: initial; border-bottom-color: initial; border-left-style: solid; border-left-color: transparent; }
.dropdown-toggle:empty::after { margin-left: 0px; }
.dropdown-menu { position: absolute; top: 100%; left: 0px; z-index: 1000; display: none; float: left; min-width: 10rem; padding: 0.5rem 0px; margin: 0.125rem 0px 0px; font-size: 0.85rem; color: rgb(133, 135, 150); text-align: left; list-style: none; background-color: rgb(255, 255, 255); background-clip: padding-box; border: 1px solid rgb(227, 230, 240); border-radius: 0.35rem; }
.dropdown-menu-left { right: auto; left: 0px; }
.dropdown-menu-right { right: 0px; left: auto; }
@media (min-width: 576px) {
  .dropdown-menu-sm-left { right: auto; left: 0px; }
  .dropdown-menu-sm-right { right: 0px; left: auto; }
}
@media (min-width: 768px) {
  .dropdown-menu-md-left { right: auto; left: 0px; }
  .dropdown-menu-md-right { right: 0px; left: auto; }
}
@media (min-width: 992px) {
  .dropdown-menu-lg-left { right: auto; left: 0px; }
  .dropdown-menu-lg-right { right: 0px; left: auto; }
}
@media (min-width: 1200px) {
  .dropdown-menu-xl-left { right: auto; left: 0px; }
  .dropdown-menu-xl-right { right: 0px; left: auto; }
}
.dropup .dropdown-menu { top: auto; bottom: 100%; margin-top: 0px; margin-bottom: 0.125rem; }
.dropup .dropdown-toggle::after { display: inline-block; margin-left: 0.255em; vertical-align: 0.255em; content: ""; border-width: 0px 0.3em 0.3em; border-top-style: initial; border-top-color: initial; border-right-style: solid; border-right-color: transparent; border-bottom-style: solid; border-bottom-color: initial; border-left-style: solid; border-left-color: transparent; }
.dropup .dropdown-toggle:empty::after { margin-left: 0px; }
.dropright .dropdown-menu { top: 0px; right: auto; left: 100%; margin-top: 0px; margin-left: 0.125rem; }
.dropright .dropdown-toggle::after { display: inline-block; margin-left: 0.255em; vertical-align: 0.255em; content: ""; border-width: 0.3em 0px 0.3em 0.3em; border-top-style: solid; border-top-color: transparent; border-right-style: initial; border-right-color: initial; border-bottom-style: solid; border-bottom-color: transparent; border-left-style: solid; border-left-color: initial; }
.dropright .dropdown-toggle:empty::after { margin-left: 0px; }
.dropright .dropdown-toggle::after { vertical-align: 0px; }
.dropleft .dropdown-menu { top: 0px; right: 100%; left: auto; margin-top: 0px; margin-right: 0.125rem; }
.dropleft .dropdown-toggle::after { display: inline-block; margin-left: 0.255em; vertical-align: 0.255em; content: ""; }
.dropleft .dropdown-toggle::after { display: none; }
.dropleft .dropdown-toggle::before { display: inline-block; margin-right: 0.255em; vertical-align: 0.255em; content: ""; border-top: 0.3em solid transparent; border-right: 0.3em solid; border-bottom: 0.3em solid transparent; }
.dropleft .dropdown-toggle:empty::after { margin-left: 0px; }
.dropleft .dropdown-toggle::before { vertical-align: 0px; }
.dropdown-menu[x-placement^="bottom"], .dropdown-menu[x-placement^="left"], .dropdown-menu[x-placement^="right"], .dropdown-menu[x-placement^="top"] { right: auto; bottom: auto; }
.dropdown-divider { height: 0px; margin: 0.5rem 0px; overflow: hidden; border-top: 1px solid rgb(234, 236, 244); }
.dropdown-item { display: block; width: 100%; padding: 0.25rem 1.5rem; clear: both; font-weight: 400; color: rgb(58, 59, 69); text-align: inherit; white-space: nowrap; background-color: transparent; border: 0px; }
.dropdown-item:focus, .dropdown-item:hover { color: rgb(46, 47, 55); text-decoration: none; background-color: rgb(234, 236, 244); }
.dropdown-item.active, .dropdown-item:active { color: rgb(255, 255, 255); text-decoration: none; background-color: rgb(78, 115, 223); }
.dropdown-item.disabled, .dropdown-item:disabled { color: rgb(183, 185, 204); pointer-events: none; background-color: transparent; }
.dropdown-menu.show { display: block; }
.dropdown-header { display: block; padding: 0.5rem 1.5rem; margin-bottom: 0px; font-size: 0.875rem; color: rgb(133, 135, 150); white-space: nowrap; }
.dropdown-item-text { display: block; padding: 0.25rem 1.5rem; color: rgb(58, 59, 69); }
.btn-group, .btn-group-vertical { position: relative; display: inline-flex; vertical-align: middle; }
.btn-group-vertical > .btn, .btn-group > .btn { position: relative; flex: 1 1 auto; }
.btn-group-vertical > .btn:hover, .btn-group > .btn:hover { z-index: 1; }
.btn-group-vertical > .btn.active, .btn-group-vertical > .btn:active, .btn-group-vertical > .btn:focus, .btn-group > .btn.active, .btn-group > .btn:active, .btn-group > .btn:focus { z-index: 1; }
.btn-toolbar { display: flex; flex-wrap: wrap; justify-content: flex-start; }
.btn-toolbar .input-group { width: auto; }
.btn-group > .btn-group:not(:first-child), .btn-group > .btn:not(:first-child) { margin-left: -1px; }
.btn-group > .btn-group:not(:last-child) > .btn, .btn-group > .btn:not(:last-child):not(.dropdown-toggle) { border-top-right-radius: 0px; border-bottom-right-radius: 0px; }
.btn-group > .btn-group:not(:first-child) > .btn, .btn-group > .btn:not(:first-child) { border-top-left-radius: 0px; border-bottom-left-radius: 0px; }
.dropdown-toggle-split { padding-right: 0.5625rem; padding-left: 0.5625rem; }
.dropdown-toggle-split::after, .dropright .dropdown-toggle-split::after, .dropup .dropdown-toggle-split::after { margin-left: 0px; }
.dropleft .dropdown-toggle-split::before { margin-right: 0px; }
.btn-group-sm > .btn + .dropdown-toggle-split, .btn-sm + .dropdown-toggle-split { padding-right: 0.375rem; padding-left: 0.375rem; }
.btn-group-lg > .btn + .dropdown-toggle-split, .btn-lg + .dropdown-toggle-split { padding-right: 0.75rem; padding-left: 0.75rem; }
.btn-group-vertical { flex-direction: column; align-items: flex-start; justify-content: center; }
.btn-group-vertical > .btn, .btn-group-vertical > .btn-group { width: 100%; }
.btn-group-vertical > .btn-group:not(:first-child), .btn-group-vertical > .btn:not(:first-child) { margin-top: -1px; }
.btn-group-vertical > .btn-group:not(:last-child) > .btn, .btn-group-vertical > .btn:not(:last-child):not(.dropdown-toggle) { border-bottom-right-radius: 0px; border-bottom-left-radius: 0px; }
.btn-group-vertical > .btn-group:not(:first-child) > .btn, .btn-group-vertical > .btn:not(:first-child) { border-top-left-radius: 0px; border-top-right-radius: 0px; }
.btn-group-toggle > .btn, .btn-group-toggle > .btn-group > .btn { margin-bottom: 0px; }
.btn-group-toggle > .btn input[type="checkbox"], .btn-group-toggle > .btn input[type="radio"], .btn-group-toggle > .btn-group > .btn input[type="checkbox"], .btn-group-toggle > .btn-group > .btn input[type="radio"] { position: absolute; clip: rect(0px, 0px, 0px, 0px); pointer-events: none; }
.input-group { position: relative; display: flex; flex-wrap: wrap; align-items: stretch; width: 100%; }
.input-group > .custom-file, .input-group > .custom-select, .input-group > .form-control, .input-group > .form-control-plaintext { position: relative; flex: 1 1 auto; width: 1%; min-width: 0px; margin-bottom: 0px; }
.input-group > .custom-file + .custom-file, .input-group > .custom-file + .custom-select, .input-group > .custom-file + .form-control, .input-group > .custom-select + .custom-file, .input-group > .custom-select + .custom-select, .input-group > .custom-select + .form-control, .input-group > .form-control + .custom-file, .input-group > .form-control + .custom-select, .input-group > .form-control + .form-control, .input-group > .form-control-plaintext + .custom-file, .input-group > .form-control-plaintext + .custom-select, .input-group > .form-control-plaintext + .form-control { margin-left: -1px; }
.input-group > .custom-file .custom-file-input:focus ~ .custom-file-label, .input-group > .custom-select:focus, .input-group > .form-control:focus { z-index: 3; }
.input-group > .custom-file .custom-file-input:focus { z-index: 4; }
.input-group > .custom-select:not(:first-child), .input-group > .form-control:not(:first-child) { border-top-left-radius: 0px; border-bottom-left-radius: 0px; }
.input-group > .custom-file { display: flex; align-items: center; }
.input-group > .custom-file:not(:first-child) .custom-file-label, .input-group > .custom-file:not(:last-child) .custom-file-label { border-top-left-radius: 0px; border-bottom-left-radius: 0px; }
.input-group:not(.has-validation) > .custom-file:not(:last-child) .custom-file-label::after, .input-group:not(.has-validation) > .custom-select:not(:last-child), .input-group:not(.has-validation) > .form-control:not(:last-child) { border-top-right-radius: 0px; border-bottom-right-radius: 0px; }
.input-group.has-validation > .custom-file:nth-last-child(n+3) .custom-file-label::after, .input-group.has-validation > .custom-select:nth-last-child(n+3), .input-group.has-validation > .form-control:nth-last-child(n+3) { border-top-right-radius: 0px; border-bottom-right-radius: 0px; }
.input-group-append, .input-group-prepend { display: flex; }
.input-group-append .btn, .input-group-prepend .btn { position: relative; z-index: 2; }
.input-group-append .btn:focus, .input-group-prepend .btn:focus { z-index: 3; }
.input-group-append .btn + .btn, .input-group-append .btn + .input-group-text, .input-group-append .input-group-text + .btn, .input-group-append .input-group-text + .input-group-text, .input-group-prepend .btn + .btn, .input-group-prepend .btn + .input-group-text, .input-group-prepend .input-group-text + .btn, .input-group-prepend .input-group-text + .input-group-text { margin-left: -1px; }
.input-group-prepend { margin-right: -1px; }
.input-group-append { margin-left: -1px; }
.input-group-text { display: flex; align-items: center; padding: 0.375rem 0.75rem; margin-bottom: 0px; font-size: 1rem; font-weight: 400; line-height: 1.5; color: rgb(110, 112, 126); text-align: center; white-space: nowrap; background-color: rgb(234, 236, 244); border: 1px solid rgb(209, 211, 226); border-radius: 0.35rem; }
.input-group-text input[type="checkbox"], .input-group-text input[type="radio"] { margin-top: 0px; }
.input-group-lg > .custom-select, .input-group-lg > .form-control:not(textarea) { height: calc(1.5em + 1rem + 2px); }
.input-group-lg > .custom-select, .input-group-lg > .form-control, .input-group-lg > .input-group-append > .btn, .input-group-lg > .input-group-append > .input-group-text, .input-group-lg > .input-group-prepend > .btn, .input-group-lg > .input-group-prepend > .input-group-text { padding: 0.5rem 1rem; font-size: 1.25rem; line-height: 1.5; border-radius: 0.3rem; }
.input-group-sm > .custom-select, .input-group-sm > .form-control:not(textarea) { height: calc(1.5em + 0.5rem + 2px); }
.input-group-sm > .custom-select, .input-group-sm > .form-control, .input-group-sm > .input-group-append > .btn, .input-group-sm > .input-group-append > .input-group-text, .input-group-sm > .input-group-prepend > .btn, .input-group-sm > .input-group-prepend > .input-group-text { padding: 0.25rem 0.5rem; font-size: 0.875rem; line-height: 1.5; border-radius: 0.2rem; }
.input-group-lg > .custom-select, .input-group-sm > .custom-select { padding-right: 1.75rem; }
.input-group.has-validation > .input-group-append:nth-last-child(n+3) > .btn, .input-group.has-validation > .input-group-append:nth-last-child(n+3) > .input-group-text, .input-group:not(.has-validation) > .input-group-append:not(:last-child) > .btn, .input-group:not(.has-validation) > .input-group-append:not(:last-child) > .input-group-text, .input-group > .input-group-append:last-child > .btn:not(:last-child):not(.dropdown-toggle), .input-group > .input-group-append:last-child > .input-group-text:not(:last-child), .input-group > .input-group-prepend > .btn, .input-group > .input-group-prepend > .input-group-text { border-top-right-radius: 0px; border-bottom-right-radius: 0px; }
.input-group > .input-group-append > .btn, .input-group > .input-group-append > .input-group-text, .input-group > .input-group-prepend:first-child > .btn:not(:first-child), .input-group > .input-group-prepend:first-child > .input-group-text:not(:first-child), .input-group > .input-group-prepend:not(:first-child) > .btn, .input-group > .input-group-prepend:not(:first-child) > .input-group-text { border-top-left-radius: 0px; border-bottom-left-radius: 0px; }
.custom-control { position: relative; z-index: 1; display: block; min-height: 1.5rem; padding-left: 1.5rem; -webkit-print-color-adjust: exact; }
.custom-control-inline { display: inline-flex; margin-right: 1rem; }
.custom-control-input { position: absolute; left: 0px; z-index: -1; width: 1rem; height: 1.25rem; opacity: 0; }
.custom-control-input:checked ~ .custom-control-label::before { color: rgb(255, 255, 255); border-color: rgb(78, 115, 223); background-color: rgb(78, 115, 223); }
.custom-control-input:focus ~ .custom-control-label::before { box-shadow: rgba(78, 115, 223, 0.25) 0px 0px 0px 0.2rem; }
.custom-control-input:focus:not(:checked) ~ .custom-control-label::before { border-color: rgb(186, 200, 243); }
.custom-control-input:not(:disabled):active ~ .custom-control-label::before { color: rgb(255, 255, 255); background-color: rgb(229, 235, 250); border-color: rgb(229, 235, 250); }
.custom-control-input:disabled ~ .custom-control-label, .custom-control-input[disabled] ~ .custom-control-label { color: rgb(133, 135, 150); }
.custom-control-input:disabled ~ .custom-control-label::before, .custom-control-input[disabled] ~ .custom-control-label::before { background-color: rgb(234, 236, 244); }
.custom-control-label { position: relative; margin-bottom: 0px; vertical-align: top; }
.custom-control-label::before { position: absolute; top: 0.25rem; left: -1.5rem; display: block; width: 1rem; height: 1rem; pointer-events: none; content: ""; background-color: rgb(255, 255, 255); border: 1px solid rgb(183, 185, 204); }
.custom-control-label::after { position: absolute; top: 0.25rem; left: -1.5rem; display: block; width: 1rem; height: 1rem; content: ""; background: 50% center / 50% 50% no-repeat; }
.custom-checkbox .custom-control-label::before { border-radius: 0.35rem; }
.custom-checkbox .custom-control-input:checked ~ .custom-control-label::after { background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='8' height='8' viewBox='0 0 8 8'%3e%3cpath fill='%23fff' d='M6.564.75l-3.59 3.612-1.538-1.55L0 4.26l2.974 2.99L8 2.193z'/%3e%3c/svg%3e"); }
.custom-checkbox .custom-control-input:indeterminate ~ .custom-control-label::before { border-color: rgb(78, 115, 223); background-color: rgb(78, 115, 223); }
.custom-checkbox .custom-control-input:indeterminate ~ .custom-control-label::after { background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='4' height='4' viewBox='0 0 4 4'%3e%3cpath stroke='%23fff' d='M0 2h4'/%3e%3c/svg%3e"); }
.custom-checkbox .custom-control-input:disabled:checked ~ .custom-control-label::before { background-color: rgba(78, 115, 223, 0.5); }
.custom-checkbox .custom-control-input:disabled:indeterminate ~ .custom-control-label::before { background-color: rgba(78, 115, 223, 0.5); }
.custom-radio .custom-control-label::before { border-radius: 50%; }
.custom-radio .custom-control-input:checked ~ .custom-control-label::after { background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='%23fff'/%3e%3c/svg%3e"); }
.custom-radio .custom-control-input:disabled:checked ~ .custom-control-label::before { background-color: rgba(78, 115, 223, 0.5); }
.custom-switch { padding-left: 2.25rem; }
.custom-switch .custom-control-label::before { left: -2.25rem; width: 1.75rem; pointer-events: all; border-radius: 0.5rem; }
.custom-switch .custom-control-label::after { top: calc(0.25rem + 2px); left: calc(-2.25rem + 2px); width: calc(1rem - 4px); height: calc(1rem - 4px); background-color: rgb(183, 185, 204); border-radius: 0.5rem; transition: transform 0.15s ease-in-out 0s, background-color 0.15s ease-in-out 0s, border-color 0.15s ease-in-out 0s, box-shadow 0.15s ease-in-out 0s; }
@media (prefers-reduced-motion: reduce) {
  .custom-switch .custom-control-label::after { transition: none 0s ease 0s; }
}
.custom-switch .custom-control-input:checked ~ .custom-control-label::after { background-color: rgb(255, 255, 255); transform: translateX(0.75rem); }
.custom-switch .custom-control-input:disabled:checked ~ .custom-control-label::before { background-color: rgba(78, 115, 223, 0.5); }
.custom-select { display: inline-block; width: 100%; height: calc(1.5em + 0.75rem + 2px); padding: 0.375rem 1.75rem 0.375rem 0.75rem; font-size: 1rem; font-weight: 400; line-height: 1.5; color: rgb(110, 112, 126); vertical-align: middle; background: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='4' height='5' viewBox='0 0 4 5'%3e%3cpath fill='%235a5c69' d='M2 0L0 2h4zm0 5L0 3h4z'/%3e%3c/svg%3e") right 0.75rem center / 8px 10px no-repeat rgb(255, 255, 255); border: 1px solid rgb(209, 211, 226); border-radius: 0.35rem; appearance: none; }
.custom-select:focus { border-color: rgb(186, 200, 243); outline: 0px; box-shadow: rgba(78, 115, 223, 0.25) 0px 0px 0px 0.2rem; }
.custom-select[multiple], .custom-select[size]:not([size="1"]) { height: auto; padding-right: 0.75rem; background-image: none; }
.custom-select:disabled { color: rgb(133, 135, 150); background-color: rgb(234, 236, 244); }
.custom-select-sm { height: calc(1.5em + 0.5rem + 2px); padding-top: 0.25rem; padding-bottom: 0.25rem; padding-left: 0.5rem; font-size: 0.875rem; }
.custom-select-lg { height: calc(1.5em + 1rem + 2px); padding-top: 0.5rem; padding-bottom: 0.5rem; padding-left: 1rem; font-size: 1.25rem; }
.custom-file { position: relative; display: inline-block; width: 100%; height: calc(1.5em + 0.75rem + 2px); margin-bottom: 0px; }
.custom-file-input { position: relative; z-index: 2; width: 100%; height: calc(1.5em + 0.75rem + 2px); margin: 0px; overflow: hidden; opacity: 0; }
.custom-file-input:focus ~ .custom-file-label { border-color: rgb(186, 200, 243); box-shadow: rgba(78, 115, 223, 0.25) 0px 0px 0px 0.2rem; }
.custom-file-input:disabled ~ .custom-file-label, .custom-file-input[disabled] ~ .custom-file-label { background-color: rgb(234, 236, 244); }
.custom-file-input:lang(en) ~ .custom-file-label::after { content: "Browse"; }
.custom-file-input ~ .custom-file-label[data-browse]::after { content: attr(data-browse); }
.custom-file-label { position: absolute; top: 0px; right: 0px; left: 0px; z-index: 1; height: calc(1.5em + 0.75rem + 2px); padding: 0.375rem 0.75rem; overflow: hidden; font-weight: 400; line-height: 1.5; color: rgb(110, 112, 126); background-color: rgb(255, 255, 255); border: 1px solid rgb(209, 211, 226); border-radius: 0.35rem; }
.custom-file-label::after { position: absolute; top: 0px; right: 0px; bottom: 0px; z-index: 3; display: block; height: calc(1.5em + 0.75rem); padding: 0.375rem 0.75rem; line-height: 1.5; color: rgb(110, 112, 126); content: "Browse"; background-color: rgb(234, 236, 244); border-left: inherit; border-radius: 0px 0.35rem 0.35rem 0px; }
.custom-range { width: 100%; height: 1.4rem; padding: 0px; background-color: transparent; appearance: none; }
.custom-range:focus { outline: 0px; }
.custom-range:focus::-webkit-slider-thumb { box-shadow: rgb(255, 255, 255) 0px 0px 0px 1px, rgba(78, 115, 223, 0.25) 0px 0px 0px 0.2rem; }
.custom-range::-webkit-slider-thumb { width: 1rem; height: 1rem; margin-top: -0.25rem; background-color: rgb(78, 115, 223); border: 0px; border-radius: 1rem; transition: background-color 0.15s ease-in-out 0s, border-color 0.15s ease-in-out 0s, box-shadow 0.15s ease-in-out 0s; appearance: none; }
@media (prefers-reduced-motion: reduce) {
  .custom-range::-webkit-slider-thumb { transition: none 0s ease 0s; }
}
.custom-range::-webkit-slider-thumb:active { background-color: rgb(229, 235, 250); }
.custom-range::-webkit-slider-runnable-track { width: 100%; height: 0.5rem; color: transparent; cursor: pointer; background-color: rgb(221, 223, 235); border-color: transparent; border-radius: 1rem; }
@media (prefers-reduced-motion: reduce) {
}
@media (prefers-reduced-motion: reduce) {
}
.custom-range:disabled::-webkit-slider-thumb { background-color: rgb(183, 185, 204); }
.custom-range:disabled::-webkit-slider-runnable-track { cursor: default; }
.custom-control-label::before, .custom-file-label, .custom-select { transition: background-color 0.15s ease-in-out 0s, border-color 0.15s ease-in-out 0s, box-shadow 0.15s ease-in-out 0s; }
@media (prefers-reduced-motion: reduce) {
  .custom-control-label::before, .custom-file-label, .custom-select { transition: none 0s ease 0s; }
}
.nav { display: flex; flex-wrap: wrap; padding-left: 0px; margin-bottom: 0px; list-style: none; }
.nav-link { display: block; padding: 0.5rem 1rem; }
.nav-link:focus, .nav-link:hover { text-decoration: none; }
.nav-link.disabled { color: rgb(133, 135, 150); pointer-events: none; cursor: default; }
.nav-tabs { border-bottom: 1px solid rgb(221, 223, 235); }
.nav-tabs .nav-link { margin-bottom: -1px; border: 1px solid transparent; border-top-left-radius: 0.35rem; border-top-right-radius: 0.35rem; }
.nav-tabs .nav-link:focus, .nav-tabs .nav-link:hover { border-color: rgb(234, 236, 244) rgb(234, 236, 244) rgb(221, 223, 235); }
.nav-tabs .nav-link.disabled { color: rgb(133, 135, 150); background-color: transparent; border-color: transparent; }
.nav-tabs .nav-item.show .nav-link, .nav-tabs .nav-link.active { color: rgb(110, 112, 126); background-color: rgb(255, 255, 255); border-color: rgb(221, 223, 235) rgb(221, 223, 235) rgb(255, 255, 255); }
.nav-tabs .dropdown-menu { margin-top: -1px; border-top-left-radius: 0px; border-top-right-radius: 0px; }
.nav-pills .nav-link { border-radius: 0.35rem; }
.nav-pills .nav-link.active, .nav-pills .show > .nav-link { color: rgb(255, 255, 255); background-color: rgb(78, 115, 223); }
.nav-fill .nav-item, .nav-fill > .nav-link { flex: 1 1 auto; text-align: center; }
.nav-justified .nav-item, .nav-justified > .nav-link { flex-basis: 0px; flex-grow: 1; text-align: center; }
.tab-content > .tab-pane { display: none; }
.tab-content > .active { display: block; }
.navbar { position: relative; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; padding: 0.5rem 1rem; }
.navbar .container, .navbar .container-fluid, .navbar .container-lg, .navbar .container-md, .navbar .container-sm, .navbar .container-xl { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; }
.navbar-brand { display: inline-block; padding-top: 0.3125rem; padding-bottom: 0.3125rem; margin-right: 1rem; font-size: 1.25rem; line-height: inherit; white-space: nowrap; }
.navbar-brand:focus, .navbar-brand:hover { text-decoration: none; }
.navbar-nav { display: flex; flex-direction: column; padding-left: 0px; margin-bottom: 0px; list-style: none; }
.navbar-nav .nav-link { padding-right: 0px; padding-left: 0px; }
.navbar-nav .dropdown-menu { position: static; float: none; }
.navbar-text { display: inline-block; padding-top: 0.5rem; padding-bottom: 0.5rem; }
.navbar-collapse { flex-basis: 100%; flex-grow: 1; align-items: center; }
.navbar-toggler { padding: 0.25rem 0.75rem; font-size: 1.25rem; line-height: 1; background-color: transparent; border: 1px solid transparent; border-radius: 0.35rem; }
.navbar-toggler:focus, .navbar-toggler:hover { text-decoration: none; }
.navbar-toggler-icon { display: inline-block; width: 1.5em; height: 1.5em; vertical-align: middle; content: ""; background: 50% center / 100% 100% no-repeat; }
.navbar-nav-scroll { max-height: 75vh; overflow-y: auto; }
@media (max-width: 575.98px) {
  .navbar-expand-sm > .container, .navbar-expand-sm > .container-fluid, .navbar-expand-sm > .container-lg, .navbar-expand-sm > .container-md, .navbar-expand-sm > .container-sm, .navbar-expand-sm > .container-xl { padding-right: 0px; padding-left: 0px; }
}
@media (min-width: 576px) {
  .navbar-expand-sm { flex-flow: row; justify-content: flex-start; }
  .navbar-expand-sm .navbar-nav { flex-direction: row; }
  .navbar-expand-sm .navbar-nav .dropdown-menu { position: absolute; }
  .navbar-expand-sm .navbar-nav .nav-link { padding-right: 0.5rem; padding-left: 0.5rem; }
  .navbar-expand-sm > .container, .navbar-expand-sm > .container-fluid, .navbar-expand-sm > .container-lg, .navbar-expand-sm > .container-md, .navbar-expand-sm > .container-sm, .navbar-expand-sm > .container-xl { flex-wrap: nowrap; }
  .navbar-expand-sm .navbar-nav-scroll { overflow: visible; }
  .navbar-expand-sm .navbar-collapse { flex-basis: auto; display: flex !important; }
  .navbar-expand-sm .navbar-toggler { display: none; }
}
@media (max-width: 767.98px) {
  .navbar-expand-md > .container, .navbar-expand-md > .container-fluid, .navbar-expand-md > .container-lg, .navbar-expand-md > .container-md, .navbar-expand-md > .container-sm, .navbar-expand-md > .container-xl { padding-right: 0px; padding-left: 0px; }
}
@media (min-width: 768px) {
  .navbar-expand-md { flex-flow: row; justify-content: flex-start; }
  .navbar-expand-md .navbar-nav { flex-direction: row; }
  .navbar-expand-md .navbar-nav .dropdown-menu { position: absolute; }
  .navbar-expand-md .navbar-nav .nav-link { padding-right: 0.5rem; padding-left: 0.5rem; }
  .navbar-expand-md > .container, .navbar-expand-md > .container-fluid, .navbar-expand-md > .container-lg, .navbar-expand-md > .container-md, .navbar-expand-md > .container-sm, .navbar-expand-md > .container-xl { flex-wrap: nowrap; }
  .navbar-expand-md .navbar-nav-scroll { overflow: visible; }
  .navbar-expand-md .navbar-collapse { flex-basis: auto; display: flex !important; }
  .navbar-expand-md .navbar-toggler { display: none; }
}
@media (max-width: 991.98px) {
  .navbar-expand-lg > .container, .navbar-expand-lg > .container-fluid, .navbar-expand-lg > .container-lg, .navbar-expand-lg > .container-md, .navbar-expand-lg > .container-sm, .navbar-expand-lg > .container-xl { padding-right: 0px; padding-left: 0px; }
}
@media (min-width: 992px) {
  .navbar-expand-lg { flex-flow: row; justify-content: flex-start; }
  .navbar-expand-lg .navbar-nav { flex-direction: row; }
  .navbar-expand-lg .navbar-nav .dropdown-menu { position: absolute; }
  .navbar-expand-lg .navbar-nav .nav-link { padding-right: 0.5rem; padding-left: 0.5rem; }
  .navbar-expand-lg > .container, .navbar-expand-lg > .container-fluid, .navbar-expand-lg > .container-lg, .navbar-expand-lg > .container-md, .navbar-expand-lg > .container-sm, .navbar-expand-lg > .container-xl { flex-wrap: nowrap; }
  .navbar-expand-lg .navbar-nav-scroll { overflow: visible; }
  .navbar-expand-lg .navbar-collapse { flex-basis: auto; display: flex !important; }
  .navbar-expand-lg .navbar-toggler { display: none; }
}
@media (max-width: 1199.98px) {
  .navbar-expand-xl > .container, .navbar-expand-xl > .container-fluid, .navbar-expand-xl > .container-lg, .navbar-expand-xl > .container-md, .navbar-expand-xl > .container-sm, .navbar-expand-xl > .container-xl { padding-right: 0px; padding-left: 0px; }
}
@media (min-width: 1200px) {
  .navbar-expand-xl { flex-flow: row; justify-content: flex-start; }
  .navbar-expand-xl .navbar-nav { flex-direction: row; }
  .navbar-expand-xl .navbar-nav .dropdown-menu { position: absolute; }
  .navbar-expand-xl .navbar-nav .nav-link { padding-right: 0.5rem; padding-left: 0.5rem; }
  .navbar-expand-xl > .container, .navbar-expand-xl > .container-fluid, .navbar-expand-xl > .container-lg, .navbar-expand-xl > .container-md, .navbar-expand-xl > .container-sm, .navbar-expand-xl > .container-xl { flex-wrap: nowrap; }
  .navbar-expand-xl .navbar-nav-scroll { overflow: visible; }
  .navbar-expand-xl .navbar-collapse { flex-basis: auto; display: flex !important; }
  .navbar-expand-xl .navbar-toggler { display: none; }
}
.navbar-expand { flex-flow: row; justify-content: flex-start; }
.navbar-expand > .container, .navbar-expand > .container-fluid, .navbar-expand > .container-lg, .navbar-expand > .container-md, .navbar-expand > .container-sm, .navbar-expand > .container-xl { padding-right: 0px; padding-left: 0px; }
.navbar-expand .navbar-nav { flex-direction: row; }
.navbar-expand .navbar-nav .dropdown-menu { position: absolute; }
.navbar-expand .navbar-nav .nav-link { padding-right: 0.5rem; padding-left: 0.5rem; }
.navbar-expand > .container, .navbar-expand > .container-fluid, .navbar-expand > .container-lg, .navbar-expand > .container-md, .navbar-expand > .container-sm, .navbar-expand > .container-xl { flex-wrap: nowrap; }
.navbar-expand .navbar-nav-scroll { overflow: visible; }
.navbar-expand .navbar-collapse { flex-basis: auto; display: flex !important; }
.navbar-expand .navbar-toggler { display: none; }
.navbar-light .navbar-brand { color: rgba(0, 0, 0, 0.9); }
.navbar-light .navbar-brand:focus, .navbar-light .navbar-brand:hover { color: rgba(0, 0, 0, 0.9); }
.navbar-light .navbar-nav .nav-link { color: rgba(0, 0, 0, 0.5); }
.navbar-light .navbar-nav .nav-link:focus, .navbar-light .navbar-nav .nav-link:hover { color: rgba(0, 0, 0, 0.7); }
.navbar-light .navbar-nav .nav-link.disabled { color: rgba(0, 0, 0, 0.3); }
.navbar-light .navbar-nav .active > .nav-link, .navbar-light .navbar-nav .nav-link.active, .navbar-light .navbar-nav .nav-link.show, .navbar-light .navbar-nav .show > .nav-link { color: rgba(0, 0, 0, 0.9); }
.navbar-light .navbar-toggler { color: rgba(0, 0, 0, 0.5); border-color: rgba(0, 0, 0, 0.1); }
.navbar-light .navbar-toggler-icon { background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='30' height='30' viewBox='0 0 30 30'%3e%3cpath stroke='rgba%280, 0, 0, 0.5%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e"); }
.navbar-light .navbar-text { color: rgba(0, 0, 0, 0.5); }
.navbar-light .navbar-text a { color: rgba(0, 0, 0, 0.9); }
.navbar-light .navbar-text a:focus, .navbar-light .navbar-text a:hover { color: rgba(0, 0, 0, 0.9); }
.navbar-dark .navbar-brand { color: rgb(255, 255, 255); }
.navbar-dark .navbar-brand:focus, .navbar-dark .navbar-brand:hover { color: rgb(255, 255, 255); }
.navbar-dark .navbar-nav .nav-link { color: rgba(255, 255, 255, 0.5); }
.navbar-dark .navbar-nav .nav-link:focus, .navbar-dark .navbar-nav .nav-link:hover { color: rgba(255, 255, 255, 0.75); }
.navbar-dark .navbar-nav .nav-link.disabled { color: rgba(255, 255, 255, 0.25); }
.navbar-dark .navbar-nav .active > .nav-link, .navbar-dark .navbar-nav .nav-link.active, .navbar-dark .navbar-nav .nav-link.show, .navbar-dark .navbar-nav .show > .nav-link { color: rgb(255, 255, 255); }
.navbar-dark .navbar-toggler { color: rgba(255, 255, 255, 0.5); border-color: rgba(255, 255, 255, 0.1); }
.navbar-dark .navbar-toggler-icon { background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='30' height='30' viewBox='0 0 30 30'%3e%3cpath stroke='rgba%28255, 255, 255, 0.5%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e"); }
.navbar-dark .navbar-text { color: rgba(255, 255, 255, 0.5); }
.navbar-dark .navbar-text a { color: rgb(255, 255, 255); }
.navbar-dark .navbar-text a:focus, .navbar-dark .navbar-text a:hover { color: rgb(255, 255, 255); }
.card { position: relative; display: flex; flex-direction: column; min-width: 0px; overflow-wrap: break-word; background-color: rgb(255, 255, 255); background-clip: border-box; border: 1px solid rgb(227, 230, 240); border-radius: 0.35rem; }
.card > hr { margin-right: 0px; margin-left: 0px; }
.card > .list-group { border-top: inherit; border-bottom: inherit; }
.card > .list-group:first-child { border-top-width: 0px; border-top-left-radius: calc(0.35rem - 1px); border-top-right-radius: calc(0.35rem - 1px); }
.card > .list-group:last-child { border-bottom-width: 0px; border-bottom-right-radius: calc(0.35rem - 1px); border-bottom-left-radius: calc(0.35rem - 1px); }
.card > .card-header + .list-group, .card > .list-group + .card-footer { border-top: 0px; }
.card-body { flex: 1 1 auto; min-height: 1px; padding: 1.25rem; }
.card-title { margin-bottom: 0.75rem; }
.card-subtitle { margin-top: -0.375rem; margin-bottom: 0px; }
.card-text:last-child { margin-bottom: 0px; }
.card-link:hover { text-decoration: none; }
.card-link + .card-link { margin-left: 1.25rem; }
.card-header { padding: 0.75rem 1.25rem; margin-bottom: 0px; background-color: rgb(248, 249, 252); border-bottom: 1px solid rgb(227, 230, 240); }
.card-header:first-child { border-radius: calc(0.35rem - 1px) calc(0.35rem - 1px) 0px 0px; }
.card-footer { padding: 0.75rem 1.25rem; background-color: rgb(248, 249, 252); border-top: 1px solid rgb(227, 230, 240); }
.card-footer:last-child { border-radius: 0px 0px calc(0.35rem - 1px) calc(0.35rem - 1px); }
.card-header-tabs { margin-right: -0.625rem; margin-bottom: -0.75rem; margin-left: -0.625rem; border-bottom: 0px; }
.card-header-pills { margin-right: -0.625rem; margin-left: -0.625rem; }
.card-img-overlay { position: absolute; inset: 0px; padding: 1.25rem; border-radius: calc(0.35rem - 1px); }
.card-img, .card-img-bottom, .card-img-top { flex-shrink: 0; width: 100%; }
.card-img, .card-img-top { border-top-left-radius: calc(0.35rem - 1px); border-top-right-radius: calc(0.35rem - 1px); }
.card-img, .card-img-bottom { border-bottom-right-radius: calc(0.35rem - 1px); border-bottom-left-radius: calc(0.35rem - 1px); }
.card-deck .card { margin-bottom: 0.75rem; }
@media (min-width: 576px) {
  .card-deck { display: flex; flex-flow: wrap; margin-right: -0.75rem; margin-left: -0.75rem; }
  .card-deck .card { flex: 1 0 0%; margin-right: 0.75rem; margin-bottom: 0px; margin-left: 0.75rem; }
}
.card-group > .card { margin-bottom: 0.75rem; }
@media (min-width: 576px) {
  .card-group { display: flex; flex-flow: wrap; }
  .card-group > .card { flex: 1 0 0%; margin-bottom: 0px; }
  .card-group > .card + .card { margin-left: 0px; border-left: 0px; }
  .card-group > .card:not(:last-child) { border-top-right-radius: 0px; border-bottom-right-radius: 0px; }
  .card-group > .card:not(:last-child) .card-header, .card-group > .card:not(:last-child) .card-img-top { border-top-right-radius: 0px; }
  .card-group > .card:not(:last-child) .card-footer, .card-group > .card:not(:last-child) .card-img-bottom { border-bottom-right-radius: 0px; }
  .card-group > .card:not(:first-child) { border-top-left-radius: 0px; border-bottom-left-radius: 0px; }
  .card-group > .card:not(:first-child) .card-header, .card-group > .card:not(:first-child) .card-img-top { border-top-left-radius: 0px; }
  .card-group > .card:not(:first-child) .card-footer, .card-group > .card:not(:first-child) .card-img-bottom { border-bottom-left-radius: 0px; }
}
.card-columns .card { margin-bottom: 0.75rem; }
@media (min-width: 576px) {
  .card-columns { column-count: 3; column-gap: 1.25rem; orphans: 1; widows: 1; }
  .card-columns .card { display: inline-block; width: 100%; }
}
.accordion { overflow-anchor: none; }
.accordion > .card { overflow: hidden; }
.accordion > .card:not(:last-of-type) { border-bottom: 0px; border-bottom-right-radius: 0px; border-bottom-left-radius: 0px; }
.accordion > .card:not(:first-of-type) { border-top-left-radius: 0px; border-top-right-radius: 0px; }
.accordion > .card > .card-header { border-radius: 0px; margin-bottom: -1px; }
.breadcrumb { display: flex; flex-wrap: wrap; padding: 0.75rem 1rem; margin-bottom: 1rem; list-style: none; background-color: rgb(234, 236, 244); border-radius: 0.35rem; }
.breadcrumb-item + .breadcrumb-item { padding-left: 0.5rem; }
.breadcrumb-item + .breadcrumb-item::before { float: left; padding-right: 0.5rem; color: rgb(133, 135, 150); content: "/"; }
.breadcrumb-item + .breadcrumb-item:hover::before { text-decoration: underline; }
.breadcrumb-item + .breadcrumb-item:hover::before { text-decoration: none; }
.breadcrumb-item.active { color: rgb(133, 135, 150); }
.pagination { display: flex; padding-left: 0px; list-style: none; border-radius: 0.35rem; }
.page-link { position: relative; display: block; padding: 0.5rem 0.75rem; margin-left: -1px; line-height: 1.25; color: rgb(78, 115, 223); background-color: rgb(255, 255, 255); border: 1px solid rgb(221, 223, 235); }
.page-link:hover { z-index: 2; color: rgb(34, 74, 190); text-decoration: none; background-color: rgb(234, 236, 244); border-color: rgb(221, 223, 235); }
.page-link:focus { z-index: 3; outline: 0px; box-shadow: rgba(78, 115, 223, 0.25) 0px 0px 0px 0.2rem; }
.page-item:first-child .page-link { margin-left: 0px; border-top-left-radius: 0.35rem; border-bottom-left-radius: 0.35rem; }
.page-item:last-child .page-link { border-top-right-radius: 0.35rem; border-bottom-right-radius: 0.35rem; }
.page-item.active .page-link { z-index: 3; color: rgb(255, 255, 255); background-color: rgb(78, 115, 223); border-color: rgb(78, 115, 223); }
.page-item.disabled .page-link { color: rgb(133, 135, 150); pointer-events: none; cursor: auto; background-color: rgb(255, 255, 255); border-color: rgb(221, 223, 235); }
.pagination-lg .page-link { padding: 0.75rem 1.5rem; font-size: 1.25rem; line-height: 1.5; }
.pagination-lg .page-item:first-child .page-link { border-top-left-radius: 0.3rem; border-bottom-left-radius: 0.3rem; }
.pagination-lg .page-item:last-child .page-link { border-top-right-radius: 0.3rem; border-bottom-right-radius: 0.3rem; }
.pagination-sm .page-link { padding: 0.25rem 0.5rem; font-size: 0.875rem; line-height: 1.5; }
.pagination-sm .page-item:first-child .page-link { border-top-left-radius: 0.2rem; border-bottom-left-radius: 0.2rem; }
.pagination-sm .page-item:last-child .page-link { border-top-right-radius: 0.2rem; border-bottom-right-radius: 0.2rem; }
.badge { display: inline-block; padding: 0.25em 0.4em; font-size: 75%; font-weight: 700; line-height: 1; text-align: center; white-space: nowrap; vertical-align: baseline; border-radius: 0.35rem; transition: color 0.15s ease-in-out 0s, background-color 0.15s ease-in-out 0s, border-color 0.15s ease-in-out 0s, box-shadow 0.15s ease-in-out 0s; }
@media (prefers-reduced-motion: reduce) {
  .badge { transition: none 0s ease 0s; }
}
a.badge:focus, a.badge:hover { text-decoration: none; }
.badge:empty { display: none; }
.btn .badge { position: relative; top: -1px; }
.badge-pill { padding-right: 0.6em; padding-left: 0.6em; border-radius: 10rem; }
.badge-primary { color: rgb(255, 255, 255); background-color: rgb(78, 115, 223); }
a.badge-primary:focus, a.badge-primary:hover { color: rgb(255, 255, 255); background-color: rgb(38, 83, 212); }
a.badge-primary.focus, a.badge-primary:focus { outline: 0px; box-shadow: rgba(78, 115, 223, 0.5) 0px 0px 0px 0.2rem; }
.badge-secondary { color: rgb(255, 255, 255); background-color: rgb(133, 135, 150); }
a.badge-secondary:focus, a.badge-secondary:hover { color: rgb(255, 255, 255); background-color: rgb(107, 109, 125); }
a.badge-secondary.focus, a.badge-secondary:focus { outline: 0px; box-shadow: rgba(133, 135, 150, 0.5) 0px 0px 0px 0.2rem; }
.badge-success { color: rgb(255, 255, 255); background-color: rgb(28, 200, 138); }
a.badge-success:focus, a.badge-success:hover { color: rgb(255, 255, 255); background-color: rgb(22, 155, 107); }
a.badge-success.focus, a.badge-success:focus { outline: 0px; box-shadow: rgba(28, 200, 138, 0.5) 0px 0px 0px 0.2rem; }
.badge-info { color: rgb(255, 255, 255); background-color: rgb(54, 185, 204); }
a.badge-info:focus, a.badge-info:hover { color: rgb(255, 255, 255); background-color: rgb(42, 150, 165); }
a.badge-info.focus, a.badge-info:focus { outline: 0px; box-shadow: rgba(54, 185, 204, 0.5) 0px 0px 0px 0.2rem; }
.badge-warning { color: rgb(255, 255, 255); background-color: rgb(246, 194, 62); }
a.badge-warning:focus, a.badge-warning:hover { color: rgb(255, 255, 255); background-color: rgb(244, 179, 13); }
a.badge-warning.focus, a.badge-warning:focus { outline: 0px; box-shadow: rgba(246, 194, 62, 0.5) 0px 0px 0px 0.2rem; }
.badge-danger { color: rgb(255, 255, 255); background-color: rgb(231, 74, 59); }
a.badge-danger:focus, a.badge-danger:hover { color: rgb(255, 255, 255); background-color: rgb(213, 42, 26); }
a.badge-danger.focus, a.badge-danger:focus { outline: 0px; box-shadow: rgba(231, 74, 59, 0.5) 0px 0px 0px 0.2rem; }
.badge-light { color: rgb(58, 59, 69); background-color: rgb(248, 249, 252); }
a.badge-light:focus, a.badge-light:hover { color: rgb(58, 59, 69); background-color: rgb(212, 218, 237); }
a.badge-light.focus, a.badge-light:focus { outline: 0px; box-shadow: rgba(248, 249, 252, 0.5) 0px 0px 0px 0.2rem; }
.badge-dark { color: rgb(255, 255, 255); background-color: rgb(90, 92, 105); }
a.badge-dark:focus, a.badge-dark:hover { color: rgb(255, 255, 255); background-color: rgb(66, 68, 78); }
a.badge-dark.focus, a.badge-dark:focus { outline: 0px; box-shadow: rgba(90, 92, 105, 0.5) 0px 0px 0px 0.2rem; }
.jumbotron { padding: 2rem 1rem; margin-bottom: 2rem; background-color: rgb(234, 236, 244); border-radius: 0.3rem; }
@media (min-width: 576px) {
  .jumbotron { padding: 4rem 2rem; }
}
.jumbotron-fluid { padding-right: 0px; padding-left: 0px; border-radius: 0px; }
.alert { position: relative; padding: 0.75rem 1.25rem; margin-bottom: 1rem; border: 1px solid transparent; border-radius: 0.35rem; }
.alert-heading { color: inherit; }
.alert-link { font-weight: 700; }
.alert-dismissible { padding-right: 4rem; }
.alert-dismissible .close { position: absolute; top: 0px; right: 0px; z-index: 2; padding: 0.75rem 1.25rem; color: inherit; }
.alert-primary { color: rgb(41, 60, 116); background-color: rgb(220, 227, 249); border-color: rgb(205, 216, 246); }
.alert-primary hr { border-top-color: rgb(183, 199, 242); }
.alert-primary .alert-link { color: rgb(28, 41, 78); }
.alert-secondary { color: rgb(69, 70, 78); background-color: rgb(231, 231, 234); border-color: rgb(221, 221, 226); }
.alert-secondary hr { border-top-color: rgb(207, 207, 214); }
.alert-secondary .alert-link { color: rgb(45, 46, 51); }
.alert-success { color: rgb(15, 104, 72); background-color: rgb(210, 244, 232); border-color: rgb(191, 240, 222); }
.alert-success hr { border-top-color: rgb(170, 235, 211); }
.alert-success .alert-link { color: rgb(9, 59, 41); }
.alert-info { color: rgb(28, 96, 106); background-color: rgb(215, 241, 245); border-color: rgb(199, 235, 241); }
.alert-info hr { border-top-color: rgb(179, 228, 236); }
.alert-info .alert-link { color: rgb(17, 59, 66); }
.alert-warning { color: rgb(128, 101, 32); background-color: rgb(253, 243, 216); border-color: rgb(252, 238, 201); }
.alert-warning hr { border-top-color: rgb(251, 230, 177); }
.alert-warning .alert-link { color: rgb(87, 69, 22); }
.alert-danger { color: rgb(120, 38, 31); background-color: rgb(250, 219, 216); border-color: rgb(248, 204, 200); }
.alert-danger hr { border-top-color: rgb(245, 183, 177); }
.alert-danger .alert-link { color: rgb(79, 25, 21); }
.alert-light { color: rgb(129, 129, 131); background-color: rgb(254, 254, 254); border-color: rgb(253, 253, 254); }
.alert-light hr { border-top-color: rgb(236, 236, 246); }
.alert-light .alert-link { color: rgb(104, 104, 105); }
.alert-dark { color: rgb(47, 48, 55); background-color: rgb(222, 222, 225); border-color: rgb(209, 209, 213); }
.alert-dark hr { border-top-color: rgb(196, 196, 201); }
.alert-dark .alert-link { color: rgb(24, 24, 28); }
@-webkit-keyframes progress-bar-stripes { 
  0% { background-position: 1rem 0px; }
  100% { background-position: 0px 0px; }
}
@keyframes progress-bar-stripes { 
  0% { background-position: 1rem 0px; }
  100% { background-position: 0px 0px; }
}
.progress { display: flex; height: 1rem; overflow: hidden; line-height: 0; font-size: 0.75rem; background-color: rgb(234, 236, 244); border-radius: 0.35rem; }
.progress-bar { display: flex; flex-direction: column; justify-content: center; overflow: hidden; color: rgb(255, 255, 255); text-align: center; white-space: nowrap; background-color: rgb(78, 115, 223); transition: width 0.6s ease 0s; }
@media (prefers-reduced-motion: reduce) {
  .progress-bar { transition: none 0s ease 0s; }
}
.progress-bar-striped { background-image: linear-gradient(45deg, rgba(255, 255, 255, 0.15) 25%, transparent 25%, transparent 50%, rgba(255, 255, 255, 0.15) 50%, rgba(255, 255, 255, 0.15) 75%, transparent 75%, transparent); background-size: 1rem 1rem; }
.progress-bar-animated { animation: 1s linear 0s infinite normal none running progress-bar-stripes; }
@media (prefers-reduced-motion: reduce) {
  .progress-bar-animated { animation: auto ease 0s 1 normal none running none; }
}
.media { display: flex; align-items: flex-start; }
.media-body { flex: 1 1 0%; }
.list-group { display: flex; flex-direction: column; padding-left: 0px; margin-bottom: 0px; border-radius: 0.35rem; }
.list-group-item-action { width: 100%; color: rgb(110, 112, 126); text-align: inherit; }
.list-group-item-action:focus, .list-group-item-action:hover { z-index: 1; color: rgb(110, 112, 126); text-decoration: none; background-color: rgb(248, 249, 252); }
.list-group-item-action:active { color: rgb(133, 135, 150); background-color: rgb(234, 236, 244); }
.list-group-item { position: relative; display: block; padding: 0.75rem 1.25rem; background-color: rgb(255, 255, 255); border: 1px solid rgba(0, 0, 0, 0.125); }
.list-group-item:first-child { border-top-left-radius: inherit; border-top-right-radius: inherit; }
.list-group-item:last-child { border-bottom-right-radius: inherit; border-bottom-left-radius: inherit; }
.list-group-item.disabled, .list-group-item:disabled { color: rgb(133, 135, 150); pointer-events: none; background-color: rgb(255, 255, 255); }
.list-group-item.active { z-index: 2; color: rgb(255, 255, 255); background-color: rgb(78, 115, 223); border-color: rgb(78, 115, 223); }
.list-group-item + .list-group-item { border-top-width: 0px; }
.list-group-item + .list-group-item.active { margin-top: -1px; border-top-width: 1px; }
.list-group-horizontal { flex-direction: row; }
.list-group-horizontal > .list-group-item:first-child { border-bottom-left-radius: 0.35rem; border-top-right-radius: 0px; }
.list-group-horizontal > .list-group-item:last-child { border-top-right-radius: 0.35rem; border-bottom-left-radius: 0px; }
.list-group-horizontal > .list-group-item.active { margin-top: 0px; }
.list-group-horizontal > .list-group-item + .list-group-item { border-top-width: 1px; border-left-width: 0px; }
.list-group-horizontal > .list-group-item + .list-group-item.active { margin-left: -1px; border-left-width: 1px; }
@media (min-width: 576px) {
  .list-group-horizontal-sm { flex-direction: row; }
  .list-group-horizontal-sm > .list-group-item:first-child { border-bottom-left-radius: 0.35rem; border-top-right-radius: 0px; }
  .list-group-horizontal-sm > .list-group-item:last-child { border-top-right-radius: 0.35rem; border-bottom-left-radius: 0px; }
  .list-group-horizontal-sm > .list-group-item.active { margin-top: 0px; }
  .list-group-horizontal-sm > .list-group-item + .list-group-item { border-top-width: 1px; border-left-width: 0px; }
  .list-group-horizontal-sm > .list-group-item + .list-group-item.active { margin-left: -1px; border-left-width: 1px; }
}
@media (min-width: 768px) {
  .list-group-horizontal-md { flex-direction: row; }
  .list-group-horizontal-md > .list-group-item:first-child { border-bottom-left-radius: 0.35rem; border-top-right-radius: 0px; }
  .list-group-horizontal-md > .list-group-item:last-child { border-top-right-radius: 0.35rem; border-bottom-left-radius: 0px; }
  .list-group-horizontal-md > .list-group-item.active { margin-top: 0px; }
  .list-group-horizontal-md > .list-group-item + .list-group-item { border-top-width: 1px; border-left-width: 0px; }
  .list-group-horizontal-md > .list-group-item + .list-group-item.active { margin-left: -1px; border-left-width: 1px; }
}
@media (min-width: 992px) {
  .list-group-horizontal-lg { flex-direction: row; }
  .list-group-horizontal-lg > .list-group-item:first-child { border-bottom-left-radius: 0.35rem; border-top-right-radius: 0px; }
  .list-group-horizontal-lg > .list-group-item:last-child { border-top-right-radius: 0.35rem; border-bottom-left-radius: 0px; }
  .list-group-horizontal-lg > .list-group-item.active { margin-top: 0px; }
  .list-group-horizontal-lg > .list-group-item + .list-group-item { border-top-width: 1px; border-left-width: 0px; }
  .list-group-horizontal-lg > .list-group-item + .list-group-item.active { margin-left: -1px; border-left-width: 1px; }
}
@media (min-width: 1200px) {
  .list-group-horizontal-xl { flex-direction: row; }
  .list-group-horizontal-xl > .list-group-item:first-child { border-bottom-left-radius: 0.35rem; border-top-right-radius: 0px; }
  .list-group-horizontal-xl > .list-group-item:last-child { border-top-right-radius: 0.35rem; border-bottom-left-radius: 0px; }
  .list-group-horizontal-xl > .list-group-item.active { margin-top: 0px; }
  .list-group-horizontal-xl > .list-group-item + .list-group-item { border-top-width: 1px; border-left-width: 0px; }
  .list-group-horizontal-xl > .list-group-item + .list-group-item.active { margin-left: -1px; border-left-width: 1px; }
}
.list-group-flush { border-radius: 0px; }
.list-group-flush > .list-group-item { border-width: 0px 0px 1px; }
.list-group-flush > .list-group-item:last-child { border-bottom-width: 0px; }
.list-group-item-primary { color: rgb(41, 60, 116); background-color: rgb(205, 216, 246); }
.list-group-item-primary.list-group-item-action:focus, .list-group-item-primary.list-group-item-action:hover { color: rgb(41, 60, 116); background-color: rgb(183, 199, 242); }
.list-group-item-primary.list-group-item-action.active { color: rgb(255, 255, 255); background-color: rgb(41, 60, 116); border-color: rgb(41, 60, 116); }
.list-group-item-secondary { color: rgb(69, 70, 78); background-color: rgb(221, 221, 226); }
.list-group-item-secondary.list-group-item-action:focus, .list-group-item-secondary.list-group-item-action:hover { color: rgb(69, 70, 78); background-color: rgb(207, 207, 214); }
.list-group-item-secondary.list-group-item-action.active { color: rgb(255, 255, 255); background-color: rgb(69, 70, 78); border-color: rgb(69, 70, 78); }
.list-group-item-success { color: rgb(15, 104, 72); background-color: rgb(191, 240, 222); }
.list-group-item-success.list-group-item-action:focus, .list-group-item-success.list-group-item-action:hover { color: rgb(15, 104, 72); background-color: rgb(170, 235, 211); }
.list-group-item-success.list-group-item-action.active { color: rgb(255, 255, 255); background-color: rgb(15, 104, 72); border-color: rgb(15, 104, 72); }
.list-group-item-info { color: rgb(28, 96, 106); background-color: rgb(199, 235, 241); }
.list-group-item-info.list-group-item-action:focus, .list-group-item-info.list-group-item-action:hover { color: rgb(28, 96, 106); background-color: rgb(179, 228, 236); }
.list-group-item-info.list-group-item-action.active { color: rgb(255, 255, 255); background-color: rgb(28, 96, 106); border-color: rgb(28, 96, 106); }
.list-group-item-warning { color: rgb(128, 101, 32); background-color: rgb(252, 238, 201); }
.list-group-item-warning.list-group-item-action:focus, .list-group-item-warning.list-group-item-action:hover { color: rgb(128, 101, 32); background-color: rgb(251, 230, 177); }
.list-group-item-warning.list-group-item-action.active { color: rgb(255, 255, 255); background-color: rgb(128, 101, 32); border-color: rgb(128, 101, 32); }
.list-group-item-danger { color: rgb(120, 38, 31); background-color: rgb(248, 204, 200); }
.list-group-item-danger.list-group-item-action:focus, .list-group-item-danger.list-group-item-action:hover { color: rgb(120, 38, 31); background-color: rgb(245, 183, 177); }
.list-group-item-danger.list-group-item-action.active { color: rgb(255, 255, 255); background-color: rgb(120, 38, 31); border-color: rgb(120, 38, 31); }
.list-group-item-light { color: rgb(129, 129, 131); background-color: rgb(253, 253, 254); }
.list-group-item-light.list-group-item-action:focus, .list-group-item-light.list-group-item-action:hover { color: rgb(129, 129, 131); background-color: rgb(236, 236, 246); }
.list-group-item-light.list-group-item-action.active { color: rgb(255, 255, 255); background-color: rgb(129, 129, 131); border-color: rgb(129, 129, 131); }
.list-group-item-dark { color: rgb(47, 48, 55); background-color: rgb(209, 209, 213); }
.list-group-item-dark.list-group-item-action:focus, .list-group-item-dark.list-group-item-action:hover { color: rgb(47, 48, 55); background-color: rgb(196, 196, 201); }
.list-group-item-dark.list-group-item-action.active { color: rgb(255, 255, 255); background-color: rgb(47, 48, 55); border-color: rgb(47, 48, 55); }
.close { float: right; font-size: 1.5rem; font-weight: 700; line-height: 1; color: rgb(0, 0, 0); text-shadow: rgb(255, 255, 255) 0px 1px 0px; opacity: 0.5; }
.close:hover { color: rgb(0, 0, 0); text-decoration: none; }
.close:not(:disabled):not(.disabled):focus, .close:not(:disabled):not(.disabled):hover { opacity: 0.75; }
button.close { padding: 0px; background-color: transparent; border: 0px; }
a.close.disabled { pointer-events: none; }
.toast { flex-basis: 350px; max-width: 350px; font-size: 0.875rem; background-color: rgba(255, 255, 255, 0.85); background-clip: padding-box; border: 1px solid rgba(0, 0, 0, 0.1); box-shadow: rgba(0, 0, 0, 0.1) 0px 0.25rem 0.75rem; opacity: 0; border-radius: 0.25rem; }
.toast:not(:last-child) { margin-bottom: 0.75rem; }
.toast.showing { opacity: 1; }
.toast.show { display: block; opacity: 1; }
.toast.hide { display: none; }
.toast-header { display: flex; align-items: center; padding: 0.25rem 0.75rem; color: rgb(133, 135, 150); background-color: rgba(255, 255, 255, 0.85); background-clip: padding-box; border-bottom: 1px solid rgba(0, 0, 0, 0.05); border-top-left-radius: calc(0.25rem - 1px); border-top-right-radius: calc(0.25rem - 1px); }
.toast-body { padding: 0.75rem; }
.modal-open { overflow: hidden; }
.modal-open .modal { overflow: hidden auto; }
.modal { position: fixed; top: 0px; left: 0px; z-index: 1050; display: none; width: 100%; height: 100%; overflow: hidden; outline: 0px; }
.modal-dialog { position: relative; width: auto; margin: 0.5rem; pointer-events: none; }
.modal.fade .modal-dialog { transition: transform 0.3s ease-out 0s; transform: translate(0px, -50px); }
@media (prefers-reduced-motion: reduce) {
  .modal.fade .modal-dialog { transition: none 0s ease 0s; }
}
.modal.show .modal-dialog { transform: none; }
.modal.modal-static .modal-dialog { transform: scale(1.02); }
.modal-dialog-scrollable { display: flex; max-height: calc(100% - 1rem); }
.modal-dialog-scrollable .modal-content { max-height: calc(100vh - 1rem); overflow: hidden; }
.modal-dialog-scrollable .modal-footer, .modal-dialog-scrollable .modal-header { flex-shrink: 0; }
.modal-dialog-scrollable .modal-body { overflow-y: auto; }
.modal-dialog-centered { display: flex; align-items: center; min-height: calc(100% - 1rem); }
.modal-dialog-centered::before { display: block; height: min-content; content: ""; }
.modal-dialog-centered.modal-dialog-scrollable { flex-direction: column; justify-content: center; height: 100%; }
.modal-dialog-centered.modal-dialog-scrollable .modal-content { max-height: none; }
.modal-dialog-centered.modal-dialog-scrollable::before { content: none; }
.modal-content { position: relative; display: flex; flex-direction: column; width: 100%; pointer-events: auto; background-color: rgb(255, 255, 255); background-clip: padding-box; border: 1px solid rgba(0, 0, 0, 0.2); border-radius: 0.3rem; outline: 0px; }
.modal-backdrop { position: fixed; top: 0px; left: 0px; z-index: 1040; width: 100vw; height: 100vh; background-color: rgb(0, 0, 0); }
.modal-backdrop.fade { opacity: 0; }
.modal-backdrop.show { opacity: 0.5; }
.modal-header { display: flex; align-items: flex-start; justify-content: space-between; padding: 1rem; border-bottom: 1px solid rgb(227, 230, 240); border-top-left-radius: calc(0.3rem - 1px); border-top-right-radius: calc(0.3rem - 1px); }
.modal-header .close { padding: 1rem; margin: -1rem -1rem -1rem auto; }
.modal-title { margin-bottom: 0px; line-height: 1.5; }
.modal-body { position: relative; flex: 1 1 auto; padding: 1rem; }
.modal-footer { display: flex; flex-wrap: wrap; align-items: center; justify-content: flex-end; padding: 0.75rem; border-top: 1px solid rgb(227, 230, 240); border-bottom-right-radius: calc(0.3rem - 1px); border-bottom-left-radius: calc(0.3rem - 1px); }
.modal-footer > * { margin: 0.25rem; }
.modal-scrollbar-measure { position: absolute; top: -9999px; width: 50px; height: 50px; overflow: scroll; }
@media (min-width: 576px) {
  .modal-dialog { max-width: 500px; margin: 1.75rem auto; }
  .modal-dialog-scrollable { max-height: calc(100% - 3.5rem); }
  .modal-dialog-scrollable .modal-content { max-height: calc(100vh - 3.5rem); }
  .modal-dialog-centered { min-height: calc(100% - 3.5rem); }
  .modal-dialog-centered::before { height: min-content; }
  .modal-sm { max-width: 300px; }
}
@media (min-width: 992px) {
  .modal-lg, .modal-xl { max-width: 800px; }
}
@media (min-width: 1200px) {
  .modal-xl { max-width: 1140px; }
}
.tooltip { position: absolute; z-index: 1070; display: block; margin: 0px; font-family: Nunito, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"; font-style: normal; font-weight: 400; line-height: 1.5; text-align: start; text-decoration: none; text-shadow: none; text-transform: none; letter-spacing: normal; word-break: normal; word-spacing: normal; white-space: normal; line-break: auto; font-size: 0.875rem; overflow-wrap: break-word; opacity: 0; }
.tooltip.show { opacity: 0.9; }
.tooltip .arrow { position: absolute; display: block; width: 0.8rem; height: 0.4rem; }
.tooltip .arrow::before { position: absolute; content: ""; border-color: transparent; border-style: solid; }
.bs-tooltip-auto[x-placement^="top"], .bs-tooltip-top { padding: 0.4rem 0px; }
.bs-tooltip-auto[x-placement^="top"] .arrow, .bs-tooltip-top .arrow { bottom: 0px; }
.bs-tooltip-auto[x-placement^="top"] .arrow::before, .bs-tooltip-top .arrow::before { top: 0px; border-width: 0.4rem 0.4rem 0px; border-top-color: rgb(0, 0, 0); }
.bs-tooltip-auto[x-placement^="right"], .bs-tooltip-right { padding: 0px 0.4rem; }
.bs-tooltip-auto[x-placement^="right"] .arrow, .bs-tooltip-right .arrow { left: 0px; width: 0.4rem; height: 0.8rem; }
.bs-tooltip-auto[x-placement^="right"] .arrow::before, .bs-tooltip-right .arrow::before { right: 0px; border-width: 0.4rem 0.4rem 0.4rem 0px; border-right-color: rgb(0, 0, 0); }
.bs-tooltip-auto[x-placement^="bottom"], .bs-tooltip-bottom { padding: 0.4rem 0px; }
.bs-tooltip-auto[x-placement^="bottom"] .arrow, .bs-tooltip-bottom .arrow { top: 0px; }
.bs-tooltip-auto[x-placement^="bottom"] .arrow::before, .bs-tooltip-bottom .arrow::before { bottom: 0px; border-width: 0px 0.4rem 0.4rem; border-bottom-color: rgb(0, 0, 0); }
.bs-tooltip-auto[x-placement^="left"], .bs-tooltip-left { padding: 0px 0.4rem; }
.bs-tooltip-auto[x-placement^="left"] .arrow, .bs-tooltip-left .arrow { right: 0px; width: 0.4rem; height: 0.8rem; }
.bs-tooltip-auto[x-placement^="left"] .arrow::before, .bs-tooltip-left .arrow::before { left: 0px; border-width: 0.4rem 0px 0.4rem 0.4rem; border-left-color: rgb(0, 0, 0); }
.tooltip-inner { max-width: 200px; padding: 0.25rem 0.5rem; color: rgb(255, 255, 255); text-align: center; background-color: rgb(0, 0, 0); border-radius: 0.35rem; }
.popover { position: absolute; top: 0px; left: 0px; z-index: 1060; display: block; max-width: 276px; font-family: Nunito, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"; font-style: normal; font-weight: 400; line-height: 1.5; text-align: start; text-decoration: none; text-shadow: none; text-transform: none; letter-spacing: normal; word-break: normal; word-spacing: normal; white-space: normal; line-break: auto; font-size: 0.875rem; overflow-wrap: break-word; background-color: rgb(255, 255, 255); background-clip: padding-box; border: 1px solid rgba(0, 0, 0, 0.2); border-radius: 0.3rem; }
.popover .arrow { position: absolute; display: block; width: 1rem; height: 0.5rem; margin: 0px 0.3rem; }
.popover .arrow::after, .popover .arrow::before { position: absolute; display: block; content: ""; border-color: transparent; border-style: solid; }
.bs-popover-auto[x-placement^="top"], .bs-popover-top { margin-bottom: 0.5rem; }
.bs-popover-auto[x-placement^="top"] > .arrow, .bs-popover-top > .arrow { bottom: calc(-0.5rem - 1px); }
.bs-popover-auto[x-placement^="top"] > .arrow::before, .bs-popover-top > .arrow::before { bottom: 0px; border-width: 0.5rem 0.5rem 0px; border-top-color: rgba(0, 0, 0, 0.25); }
.bs-popover-auto[x-placement^="top"] > .arrow::after, .bs-popover-top > .arrow::after { bottom: 1px; border-width: 0.5rem 0.5rem 0px; border-top-color: rgb(255, 255, 255); }
.bs-popover-auto[x-placement^="right"], .bs-popover-right { margin-left: 0.5rem; }
.bs-popover-auto[x-placement^="right"] > .arrow, .bs-popover-right > .arrow { left: calc(-0.5rem - 1px); width: 0.5rem; height: 1rem; margin: 0.3rem 0px; }
.bs-popover-auto[x-placement^="right"] > .arrow::before, .bs-popover-right > .arrow::before { left: 0px; border-width: 0.5rem 0.5rem 0.5rem 0px; border-right-color: rgba(0, 0, 0, 0.25); }
.bs-popover-auto[x-placement^="right"] > .arrow::after, .bs-popover-right > .arrow::after { left: 1px; border-width: 0.5rem 0.5rem 0.5rem 0px; border-right-color: rgb(255, 255, 255); }
.bs-popover-auto[x-placement^="bottom"], .bs-popover-bottom { margin-top: 0.5rem; }
.bs-popover-auto[x-placement^="bottom"] > .arrow, .bs-popover-bottom > .arrow { top: calc(-0.5rem - 1px); }
.bs-popover-auto[x-placement^="bottom"] > .arrow::before, .bs-popover-bottom > .arrow::before { top: 0px; border-width: 0px 0.5rem 0.5rem; border-bottom-color: rgba(0, 0, 0, 0.25); }
.bs-popover-auto[x-placement^="bottom"] > .arrow::after, .bs-popover-bottom > .arrow::after { top: 1px; border-width: 0px 0.5rem 0.5rem; border-bottom-color: rgb(255, 255, 255); }
.bs-popover-auto[x-placement^="bottom"] .popover-header::before, .bs-popover-bottom .popover-header::before { position: absolute; top: 0px; left: 50%; display: block; width: 1rem; margin-left: -0.5rem; content: ""; border-bottom: 1px solid rgb(247, 247, 247); }
.bs-popover-auto[x-placement^="left"], .bs-popover-left { margin-right: 0.5rem; }
.bs-popover-auto[x-placement^="left"] > .arrow, .bs-popover-left > .arrow { right: calc(-0.5rem - 1px); width: 0.5rem; height: 1rem; margin: 0.3rem 0px; }
.bs-popover-auto[x-placement^="left"] > .arrow::before, .bs-popover-left > .arrow::before { right: 0px; border-width: 0.5rem 0px 0.5rem 0.5rem; border-left-color: rgba(0, 0, 0, 0.25); }
.bs-popover-auto[x-placement^="left"] > .arrow::after, .bs-popover-left > .arrow::after { right: 1px; border-width: 0.5rem 0px 0.5rem 0.5rem; border-left-color: rgb(255, 255, 255); }
.popover-header { padding: 0.5rem 0.75rem; margin-bottom: 0px; font-size: 1rem; background-color: rgb(247, 247, 247); border-bottom: 1px solid rgb(235, 235, 235); border-top-left-radius: calc(0.3rem - 1px); border-top-right-radius: calc(0.3rem - 1px); }
.popover-header:empty { display: none; }
.popover-body { padding: 0.5rem 0.75rem; color: rgb(133, 135, 150); }
.carousel { position: relative; }
.carousel.pointer-event { touch-action: pan-y; }
.carousel-inner { position: relative; width: 100%; overflow: hidden; }
.carousel-inner::after { display: block; clear: both; content: ""; }
.carousel-item { position: relative; display: none; float: left; width: 100%; margin-right: -100%; backface-visibility: hidden; transition: transform 0.6s ease-in-out 0s; }
@media (prefers-reduced-motion: reduce) {
  .carousel-item { transition: none 0s ease 0s; }
}
.carousel-item-next, .carousel-item-prev, .carousel-item.active { display: block; }
.active.carousel-item-right, .carousel-item-next:not(.carousel-item-left) { transform: translateX(100%); }
.active.carousel-item-left, .carousel-item-prev:not(.carousel-item-right) { transform: translateX(-100%); }
.carousel-fade .carousel-item { opacity: 0; transition-property: opacity; transform: none; }
.carousel-fade .carousel-item-next.carousel-item-left, .carousel-fade .carousel-item-prev.carousel-item-right, .carousel-fade .carousel-item.active { z-index: 1; opacity: 1; }
.carousel-fade .active.carousel-item-left, .carousel-fade .active.carousel-item-right { z-index: 0; opacity: 0; transition: opacity 0s ease 0.6s; }
@media (prefers-reduced-motion: reduce) {
  .carousel-fade .active.carousel-item-left, .carousel-fade .active.carousel-item-right { transition: none 0s ease 0s; }
}
.carousel-control-next, .carousel-control-prev { position: absolute; top: 0px; bottom: 0px; z-index: 1; display: flex; align-items: center; justify-content: center; width: 15%; color: rgb(255, 255, 255); text-align: center; opacity: 0.5; transition: opacity 0.15s ease 0s; }
@media (prefers-reduced-motion: reduce) {
  .carousel-control-next, .carousel-control-prev { transition: none 0s ease 0s; }
}
.carousel-control-next:focus, .carousel-control-next:hover, .carousel-control-prev:focus, .carousel-control-prev:hover { color: rgb(255, 255, 255); text-decoration: none; outline: 0px; opacity: 0.9; }
.carousel-control-prev { left: 0px; }
.carousel-control-next { right: 0px; }
.carousel-control-next-icon, .carousel-control-prev-icon { display: inline-block; width: 20px; height: 20px; background: 50% center / 100% 100% no-repeat; }
.carousel-control-prev-icon { background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='%23fff' width='8' height='8' viewBox='0 0 8 8'%3e%3cpath d='M5.25 0l-4 4 4 4 1.5-1.5L4.25 4l2.5-2.5L5.25 0z'/%3e%3c/svg%3e"); }
.carousel-control-next-icon { background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='%23fff' width='8' height='8' viewBox='0 0 8 8'%3e%3cpath d='M2.75 0l-1.5 1.5L3.75 4l-2.5 2.5L2.75 8l4-4-4-4z'/%3e%3c/svg%3e"); }
.carousel-indicators { position: absolute; right: 0px; bottom: 0px; left: 0px; z-index: 15; display: flex; justify-content: center; padding-left: 0px; margin-right: 15%; margin-left: 15%; list-style: none; }
.carousel-indicators li { box-sizing: content-box; flex: 0 1 auto; width: 30px; height: 3px; margin-right: 3px; margin-left: 3px; text-indent: -999px; cursor: pointer; background-color: rgb(255, 255, 255); background-clip: padding-box; border-top: 10px solid transparent; border-bottom: 10px solid transparent; opacity: 0.5; transition: opacity 0.6s ease 0s; }
@media (prefers-reduced-motion: reduce) {
  .carousel-indicators li { transition: none 0s ease 0s; }
}
.carousel-indicators .active { opacity: 1; }
.carousel-caption { position: absolute; right: 15%; bottom: 20px; left: 15%; z-index: 10; padding-top: 20px; padding-bottom: 20px; color: rgb(255, 255, 255); text-align: center; }
@-webkit-keyframes spinner-border { 
  100% { transform: rotate(360deg); }
}
@keyframes spinner-border { 
  100% { transform: rotate(360deg); }
}
.spinner-border { display: inline-block; width: 2rem; height: 2rem; vertical-align: text-bottom; border-width: 0.25em; border-style: solid; border-color: currentcolor transparent currentcolor currentcolor; border-image: initial; border-radius: 50%; animation: 0.75s linear 0s infinite normal none running spinner-border; }
.spinner-border-sm { width: 1rem; height: 1rem; border-width: 0.2em; }
@-webkit-keyframes spinner-grow { 
  0% { transform: scale(0); }
  50% { opacity: 1; transform: none; }
}
@keyframes spinner-grow { 
  0% { transform: scale(0); }
  50% { opacity: 1; transform: none; }
}
.spinner-grow { display: inline-block; width: 2rem; height: 2rem; vertical-align: text-bottom; background-color: currentcolor; border-radius: 50%; opacity: 0; animation: 0.75s linear 0s infinite normal none running spinner-grow; }
.spinner-grow-sm { width: 1rem; height: 1rem; }
@media (prefers-reduced-motion: reduce) {
  .spinner-border, .spinner-grow { animation-duration: 1.5s; }
}
.align-baseline { vertical-align: baseline !important; }
.align-top { vertical-align: top !important; }
.align-middle { vertical-align: middle !important; }
.align-bottom { vertical-align: bottom !important; }
.align-text-bottom { vertical-align: text-bottom !important; }
.align-text-top { vertical-align: text-top !important; }
.bg-primary { background-color: rgb(78, 115, 223) !important; }
a.bg-primary:focus, a.bg-primary:hover, button.bg-primary:focus, button.bg-primary:hover { background-color: rgb(38, 83, 212) !important; }
.bg-secondary { background-color: rgb(133, 135, 150) !important; }
a.bg-secondary:focus, a.bg-secondary:hover, button.bg-secondary:focus, button.bg-secondary:hover { background-color: rgb(107, 109, 125) !important; }
.bg-success { background-color: rgb(28, 200, 138) !important; }
a.bg-success:focus, a.bg-success:hover, button.bg-success:focus, button.bg-success:hover { background-color: rgb(22, 155, 107) !important; }
.bg-info { background-color: rgb(54, 185, 204) !important; }
a.bg-info:focus, a.bg-info:hover, button.bg-info:focus, button.bg-info:hover { background-color: rgb(42, 150, 165) !important; }
.bg-warning { background-color: rgb(246, 194, 62) !important; }
a.bg-warning:focus, a.bg-warning:hover, button.bg-warning:focus, button.bg-warning:hover { background-color: rgb(244, 179, 13) !important; }
.bg-danger { background-color: rgb(231, 74, 59) !important; }
a.bg-danger:focus, a.bg-danger:hover, button.bg-danger:focus, button.bg-danger:hover { background-color: rgb(213, 42, 26) !important; }
.bg-light { background-color: rgb(248, 249, 252) !important; }
a.bg-light:focus, a.bg-light:hover, button.bg-light:focus, button.bg-light:hover { background-color: rgb(212, 218, 237) !important; }
.bg-dark { background-color: rgb(90, 92, 105) !important; }
a.bg-dark:focus, a.bg-dark:hover, button.bg-dark:focus, button.bg-dark:hover { background-color: rgb(66, 68, 78) !important; }
.bg-white { background-color: rgb(255, 255, 255) !important; }
.bg-transparent { background-color: transparent !important; }
.border { border: 1px solid rgb(227, 230, 240) !important; }
.border-top { border-top: 1px solid rgb(227, 230, 240) !important; }
.border-right { border-right: 1px solid rgb(227, 230, 240) !important; }
.border-bottom { border-bottom: 1px solid rgb(227, 230, 240) !important; }
.border-left { border-left: 1px solid rgb(227, 230, 240) !important; }
.border-0 { border: 0px !important; }
.border-top-0 { border-top: 0px !important; }
.border-right-0 { border-right: 0px !important; }
.border-bottom-0 { border-bottom: 0px !important; }
.border-left-0 { border-left: 0px !important; }
.border-primary { border-color: rgb(78, 115, 223) !important; }
.border-secondary { border-color: rgb(133, 135, 150) !important; }
.border-success { border-color: rgb(28, 200, 138) !important; }
.border-info { border-color: rgb(54, 185, 204) !important; }
.border-warning { border-color: rgb(246, 194, 62) !important; }
.border-danger { border-color: rgb(231, 74, 59) !important; }
.border-light { border-color: rgb(248, 249, 252) !important; }
.border-dark { border-color: rgb(90, 92, 105) !important; }
.border-white { border-color: rgb(255, 255, 255) !important; }
.rounded-sm { border-radius: 0.2rem !important; }
.rounded { border-radius: 0.35rem !important; }
.rounded-top { border-top-left-radius: 0.35rem !important; border-top-right-radius: 0.35rem !important; }
.rounded-right { border-top-right-radius: 0.35rem !important; border-bottom-right-radius: 0.35rem !important; }
.rounded-bottom { border-bottom-right-radius: 0.35rem !important; border-bottom-left-radius: 0.35rem !important; }
.rounded-left { border-top-left-radius: 0.35rem !important; border-bottom-left-radius: 0.35rem !important; }
.rounded-lg { border-radius: 0.3rem !important; }
.rounded-circle { border-radius: 50% !important; }
.rounded-pill { border-radius: 50rem !important; }
.rounded-0 { border-radius: 0px !important; }
.clearfix::after { display: block; clear: both; content: ""; }
.d-none { display: none !important; }
.d-inline { display: inline !important; }
.d-inline-block { display: inline-block !important; }
.d-block { display: block !important; }
.d-table { display: table !important; }
.d-table-row { display: table-row !important; }
.d-table-cell { display: table-cell !important; }
.d-flex { display: flex !important; }
.d-inline-flex { display: inline-flex !important; }
@media (min-width: 576px) {
  .d-sm-none { display: none !important; }
  .d-sm-inline { display: inline !important; }
  .d-sm-inline-block { display: inline-block !important; }
  .d-sm-block { display: block !important; }
  .d-sm-table { display: table !important; }
  .d-sm-table-row { display: table-row !important; }
  .d-sm-table-cell { display: table-cell !important; }
  .d-sm-flex { display: flex !important; }
  .d-sm-inline-flex { display: inline-flex !important; }
}
@media (min-width: 768px) {
  .d-md-none { display: none !important; }
  .d-md-inline { display: inline !important; }
  .d-md-inline-block { display: inline-block !important; }
  .d-md-block { display: block !important; }
  .d-md-table { display: table !important; }
  .d-md-table-row { display: table-row !important; }
  .d-md-table-cell { display: table-cell !important; }
  .d-md-flex { display: flex !important; }
  .d-md-inline-flex { display: inline-flex !important; }
}
@media (min-width: 992px) {
  .d-lg-none { display: none !important; }
  .d-lg-inline { display: inline !important; }
  .d-lg-inline-block { display: inline-block !important; }
  .d-lg-block { display: block !important; }
  .d-lg-table { display: table !important; }
  .d-lg-table-row { display: table-row !important; }
  .d-lg-table-cell { display: table-cell !important; }
  .d-lg-flex { display: flex !important; }
  .d-lg-inline-flex { display: inline-flex !important; }
}
@media (min-width: 1200px) {
  .d-xl-none { display: none !important; }
  .d-xl-inline { display: inline !important; }
  .d-xl-inline-block { display: inline-block !important; }
  .d-xl-block { display: block !important; }
  .d-xl-table { display: table !important; }
  .d-xl-table-row { display: table-row !important; }
  .d-xl-table-cell { display: table-cell !important; }
  .d-xl-flex { display: flex !important; }
  .d-xl-inline-flex { display: inline-flex !important; }
}
@media print {
  .d-print-none { display: none !important; }
  .d-print-inline { display: inline !important; }
  .d-print-inline-block { display: inline-block !important; }
  .d-print-block { display: block !important; }
  .d-print-table { display: table !important; }
  .d-print-table-row { display: table-row !important; }
  .d-print-table-cell { display: table-cell !important; }
  .d-print-flex { display: flex !important; }
  .d-print-inline-flex { display: inline-flex !important; }
}
.embed-responsive { position: relative; display: block; width: 100%; padding: 0px; overflow: hidden; }
.embed-responsive::before { display: block; content: ""; }
.embed-responsive .embed-responsive-item, .embed-responsive embed, .embed-responsive iframe, .embed-responsive object, .embed-responsive video { position: absolute; top: 0px; bottom: 0px; left: 0px; width: 100%; height: 100%; border: 0px; }
.embed-responsive-21by9::before { padding-top: 42.8571%; }
.embed-responsive-16by9::before { padding-top: 56.25%; }
.embed-responsive-4by3::before { padding-top: 75%; }
.embed-responsive-1by1::before { padding-top: 100%; }
.flex-row { flex-direction: row !important; }
.flex-column { flex-direction: column !important; }
.flex-row-reverse { flex-direction: row-reverse !important; }
.flex-column-reverse { flex-direction: column-reverse !important; }
.flex-wrap { flex-wrap: wrap !important; }
.flex-nowrap { flex-wrap: nowrap !important; }
.flex-wrap-reverse { flex-wrap: wrap-reverse !important; }
.flex-fill { flex: 1 1 auto !important; }
.flex-grow-0 { flex-grow: 0 !important; }
.flex-grow-1 { flex-grow: 1 !important; }
.flex-shrink-0 { flex-shrink: 0 !important; }
.flex-shrink-1 { flex-shrink: 1 !important; }
.justify-content-start { justify-content: flex-start !important; }
.justify-content-end { justify-content: flex-end !important; }
.justify-content-center { justify-content: center !important; }
.justify-content-between { justify-content: space-between !important; }
.justify-content-around { justify-content: space-around !important; }
.align-items-start { align-items: flex-start !important; }
.align-items-end { align-items: flex-end !important; }
.align-items-center { align-items: center !important; }
.align-items-baseline { align-items: baseline !important; }
.align-items-stretch { align-items: stretch !important; }
.align-content-start { align-content: flex-start !important; }
.align-content-end { align-content: flex-end !important; }
.align-content-center { align-content: center !important; }
.align-content-between { align-content: space-between !important; }
.align-content-around { align-content: space-around !important; }
.align-content-stretch { align-content: stretch !important; }
.align-self-auto { align-self: auto !important; }
.align-self-start { align-self: flex-start !important; }
.align-self-end { align-self: flex-end !important; }
.align-self-center { align-self: center !important; }
.align-self-baseline { align-self: baseline !important; }
.align-self-stretch { align-self: stretch !important; }
@media (min-width: 576px) {
  .flex-sm-row { flex-direction: row !important; }
  .flex-sm-column { flex-direction: column !important; }
  .flex-sm-row-reverse { flex-direction: row-reverse !important; }
  .flex-sm-column-reverse { flex-direction: column-reverse !important; }
  .flex-sm-wrap { flex-wrap: wrap !important; }
  .flex-sm-nowrap { flex-wrap: nowrap !important; }
  .flex-sm-wrap-reverse { flex-wrap: wrap-reverse !important; }
  .flex-sm-fill { flex: 1 1 auto !important; }
  .flex-sm-grow-0 { flex-grow: 0 !important; }
  .flex-sm-grow-1 { flex-grow: 1 !important; }
  .flex-sm-shrink-0 { flex-shrink: 0 !important; }
  .flex-sm-shrink-1 { flex-shrink: 1 !important; }
  .justify-content-sm-start { justify-content: flex-start !important; }
  .justify-content-sm-end { justify-content: flex-end !important; }
  .justify-content-sm-center { justify-content: center !important; }
  .justify-content-sm-between { justify-content: space-between !important; }
  .justify-content-sm-around { justify-content: space-around !important; }
  .align-items-sm-start { align-items: flex-start !important; }
  .align-items-sm-end { align-items: flex-end !important; }
  .align-items-sm-center { align-items: center !important; }
  .align-items-sm-baseline { align-items: baseline !important; }
  .align-items-sm-stretch { align-items: stretch !important; }
  .align-content-sm-start { align-content: flex-start !important; }
  .align-content-sm-end { align-content: flex-end !important; }
  .align-content-sm-center { align-content: center !important; }
  .align-content-sm-between { align-content: space-between !important; }
  .align-content-sm-around { align-content: space-around !important; }
  .align-content-sm-stretch { align-content: stretch !important; }
  .align-self-sm-auto { align-self: auto !important; }
  .align-self-sm-start { align-self: flex-start !important; }
  .align-self-sm-end { align-self: flex-end !important; }
  .align-self-sm-center { align-self: center !important; }
  .align-self-sm-baseline { align-self: baseline !important; }
  .align-self-sm-stretch { align-self: stretch !important; }
}
@media (min-width: 768px) {
  .flex-md-row { flex-direction: row !important; }
  .flex-md-column { flex-direction: column !important; }
  .flex-md-row-reverse { flex-direction: row-reverse !important; }
  .flex-md-column-reverse { flex-direction: column-reverse !important; }
  .flex-md-wrap { flex-wrap: wrap !important; }
  .flex-md-nowrap { flex-wrap: nowrap !important; }
  .flex-md-wrap-reverse { flex-wrap: wrap-reverse !important; }
  .flex-md-fill { flex: 1 1 auto !important; }
  .flex-md-grow-0 { flex-grow: 0 !important; }
  .flex-md-grow-1 { flex-grow: 1 !important; }
  .flex-md-shrink-0 { flex-shrink: 0 !important; }
  .flex-md-shrink-1 { flex-shrink: 1 !important; }
  .justify-content-md-start { justify-content: flex-start !important; }
  .justify-content-md-end { justify-content: flex-end !important; }
  .justify-content-md-center { justify-content: center !important; }
  .justify-content-md-between { justify-content: space-between !important; }
  .justify-content-md-around { justify-content: space-around !important; }
  .align-items-md-start { align-items: flex-start !important; }
  .align-items-md-end { align-items: flex-end !important; }
  .align-items-md-center { align-items: center !important; }
  .align-items-md-baseline { align-items: baseline !important; }
  .align-items-md-stretch { align-items: stretch !important; }
  .align-content-md-start { align-content: flex-start !important; }
  .align-content-md-end { align-content: flex-end !important; }
  .align-content-md-center { align-content: center !important; }
  .align-content-md-between { align-content: space-between !important; }
  .align-content-md-around { align-content: space-around !important; }
  .align-content-md-stretch { align-content: stretch !important; }
  .align-self-md-auto { align-self: auto !important; }
  .align-self-md-start { align-self: flex-start !important; }
  .align-self-md-end { align-self: flex-end !important; }
  .align-self-md-center { align-self: center !important; }
  .align-self-md-baseline { align-self: baseline !important; }
  .align-self-md-stretch { align-self: stretch !important; }
}
@media (min-width: 992px) {
  .flex-lg-row { flex-direction: row !important; }
  .flex-lg-column { flex-direction: column !important; }
  .flex-lg-row-reverse { flex-direction: row-reverse !important; }
  .flex-lg-column-reverse { flex-direction: column-reverse !important; }
  .flex-lg-wrap { flex-wrap: wrap !important; }
  .flex-lg-nowrap { flex-wrap: nowrap !important; }
  .flex-lg-wrap-reverse { flex-wrap: wrap-reverse !important; }
  .flex-lg-fill { flex: 1 1 auto !important; }
  .flex-lg-grow-0 { flex-grow: 0 !important; }
  .flex-lg-grow-1 { flex-grow: 1 !important; }
  .flex-lg-shrink-0 { flex-shrink: 0 !important; }
  .flex-lg-shrink-1 { flex-shrink: 1 !important; }
  .justify-content-lg-start { justify-content: flex-start !important; }
  .justify-content-lg-end { justify-content: flex-end !important; }
  .justify-content-lg-center { justify-content: center !important; }
  .justify-content-lg-between { justify-content: space-between !important; }
  .justify-content-lg-around { justify-content: space-around !important; }
  .align-items-lg-start { align-items: flex-start !important; }
  .align-items-lg-end { align-items: flex-end !important; }
  .align-items-lg-center { align-items: center !important; }
  .align-items-lg-baseline { align-items: baseline !important; }
  .align-items-lg-stretch { align-items: stretch !important; }
  .align-content-lg-start { align-content: flex-start !important; }
  .align-content-lg-end { align-content: flex-end !important; }
  .align-content-lg-center { align-content: center !important; }
  .align-content-lg-between { align-content: space-between !important; }
  .align-content-lg-around { align-content: space-around !important; }
  .align-content-lg-stretch { align-content: stretch !important; }
  .align-self-lg-auto { align-self: auto !important; }
  .align-self-lg-start { align-self: flex-start !important; }
  .align-self-lg-end { align-self: flex-end !important; }
  .align-self-lg-center { align-self: center !important; }
  .align-self-lg-baseline { align-self: baseline !important; }
  .align-self-lg-stretch { align-self: stretch !important; }
}
@media (min-width: 1200px) {
  .flex-xl-row { flex-direction: row !important; }
  .flex-xl-column { flex-direction: column !important; }
  .flex-xl-row-reverse { flex-direction: row-reverse !important; }
  .flex-xl-column-reverse { flex-direction: column-reverse !important; }
  .flex-xl-wrap { flex-wrap: wrap !important; }
  .flex-xl-nowrap { flex-wrap: nowrap !important; }
  .flex-xl-wrap-reverse { flex-wrap: wrap-reverse !important; }
  .flex-xl-fill { flex: 1 1 auto !important; }
  .flex-xl-grow-0 { flex-grow: 0 !important; }
  .flex-xl-grow-1 { flex-grow: 1 !important; }
  .flex-xl-shrink-0 { flex-shrink: 0 !important; }
  .flex-xl-shrink-1 { flex-shrink: 1 !important; }
  .justify-content-xl-start { justify-content: flex-start !important; }
  .justify-content-xl-end { justify-content: flex-end !important; }
  .justify-content-xl-center { justify-content: center !important; }
  .justify-content-xl-between { justify-content: space-between !important; }
  .justify-content-xl-around { justify-content: space-around !important; }
  .align-items-xl-start { align-items: flex-start !important; }
  .align-items-xl-end { align-items: flex-end !important; }
  .align-items-xl-center { align-items: center !important; }
  .align-items-xl-baseline { align-items: baseline !important; }
  .align-items-xl-stretch { align-items: stretch !important; }
  .align-content-xl-start { align-content: flex-start !important; }
  .align-content-xl-end { align-content: flex-end !important; }
  .align-content-xl-center { align-content: center !important; }
  .align-content-xl-between { align-content: space-between !important; }
  .align-content-xl-around { align-content: space-around !important; }
  .align-content-xl-stretch { align-content: stretch !important; }
  .align-self-xl-auto { align-self: auto !important; }
  .align-self-xl-start { align-self: flex-start !important; }
  .align-self-xl-end { align-self: flex-end !important; }
  .align-self-xl-center { align-self: center !important; }
  .align-self-xl-baseline { align-self: baseline !important; }
  .align-self-xl-stretch { align-self: stretch !important; }
}
.float-left { float: left !important; }
.float-right { float: right !important; }
.float-none { float: none !important; }
@media (min-width: 576px) {
  .float-sm-left { float: left !important; }
  .float-sm-right { float: right !important; }
  .float-sm-none { float: none !important; }
}
@media (min-width: 768px) {
  .float-md-left { float: left !important; }
  .float-md-right { float: right !important; }
  .float-md-none { float: none !important; }
}
@media (min-width: 992px) {
  .float-lg-left { float: left !important; }
  .float-lg-right { float: right !important; }
  .float-lg-none { float: none !important; }
}
@media (min-width: 1200px) {
  .float-xl-left { float: left !important; }
  .float-xl-right { float: right !important; }
  .float-xl-none { float: none !important; }
}
.user-select-all { user-select: all !important; }
.user-select-auto { user-select: auto !important; }
.user-select-none { user-select: none !important; }
.overflow-auto { overflow: auto !important; }
.overflow-hidden { overflow: hidden !important; }
.position-static { position: static !important; }
.position-relative { position: relative !important; }
.position-absolute { position: absolute !important; }
.position-fixed { position: fixed !important; }
.position-sticky { position: sticky !important; }
.fixed-top { position: fixed; top: 0px; right: 0px; left: 0px; z-index: 1030; }
.fixed-bottom { position: fixed; right: 0px; bottom: 0px; left: 0px; z-index: 1030; }
@supports ((position:-webkit-sticky) or (position:sticky)) {
  .sticky-top { position: sticky; top: 0px; z-index: 1020; }
}
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0px; margin: -1px; overflow: hidden; clip: rect(0px, 0px, 0px, 0px); white-space: nowrap; border: 0px; }
.sr-only-focusable:active, .sr-only-focusable:focus { position: static; width: auto; height: auto; overflow: visible; clip: auto; white-space: normal; }
.shadow-sm { box-shadow: rgba(58, 59, 69, 0.2) 0px 0.125rem 0.25rem 0px !important; }
.shadow { box-shadow: rgba(58, 59, 69, 0.15) 0px 0.15rem 1.75rem 0px !important; }
.shadow-lg { box-shadow: rgba(0, 0, 0, 0.176) 0px 1rem 3rem !important; }
.shadow-none { box-shadow: none !important; }
.w-25 { width: 25% !important; }
.w-50 { width: 50% !important; }
.w-75 { width: 75% !important; }
.w-100 { width: 100% !important; }
.w-auto { width: auto !important; }
.h-25 { height: 25% !important; }
.h-50 { height: 50% !important; }
.h-75 { height: 75% !important; }
.h-100 { height: 100% !important; }
.h-auto { height: auto !important; }
.mw-100 { max-width: 100% !important; }
.mh-100 { max-height: 100% !important; }
.min-vw-100 { min-width: 100vw !important; }
.min-vh-100 { min-height: 100vh !important; }
.vw-100 { width: 100vw !important; }
.vh-100 { height: 100vh !important; }
.m-0 { margin: 0px !important; }
.mt-0, .my-0 { margin-top: 0px !important; }
.mr-0, .mx-0 { margin-right: 0px !important; }
.mb-0, .my-0 { margin-bottom: 0px !important; }
.ml-0, .mx-0 { margin-left: 0px !important; }
.m-1 { margin: 0.25rem !important; }
.mt-1, .my-1 { margin-top: 0.25rem !important; }
.mr-1, .mx-1 { margin-right: 0.25rem !important; }
.mb-1, .my-1 { margin-bottom: 0.25rem !important; }
.ml-1, .mx-1 { margin-left: 0.25rem !important; }
.m-2 { margin: 0.5rem !important; }
.mt-2, .my-2 { margin-top: 0.5rem !important; }
.mr-2, .mx-2 { margin-right: 0.5rem !important; }
.mb-2, .my-2 { margin-bottom: 0.5rem !important; }
.ml-2, .mx-2 { margin-left: 0.5rem !important; }
.m-3 { margin: 1rem !important; }
.mt-3, .my-3 { margin-top: 1rem !important; }
.mr-3, .mx-3 { margin-right: 1rem !important; }
.mb-3, .my-3 { margin-bottom: 1rem !important; }
.ml-3, .mx-3 { margin-left: 1rem !important; }
.m-4 { margin: 1.5rem !important; }
.mt-4, .my-4 { margin-top: 1.5rem !important; }
.mr-4, .mx-4 { margin-right: 1.5rem !important; }
.mb-4, .my-4 { margin-bottom: 1.5rem !important; }
.ml-4, .mx-4 { margin-left: 1.5rem !important; }
.m-5 { margin: 3rem !important; }
.mt-5, .my-5 { margin-top: 3rem !important; }
.mr-5, .mx-5 { margin-right: 3rem !important; }
.mb-5, .my-5 { margin-bottom: 3rem !important; }
.ml-5, .mx-5 { margin-left: 3rem !important; }
.p-0 { padding: 0px !important; }
.pt-0, .py-0 { padding-top: 0px !important; }
.pr-0, .px-0 { padding-right: 0px !important; }
.pb-0, .py-0 { padding-bottom: 0px !important; }
.pl-0, .px-0 { padding-left: 0px !important; }
.p-1 { padding: 0.25rem !important; }
.pt-1, .py-1 { padding-top: 0.25rem !important; }
.pr-1, .px-1 { padding-right: 0.25rem !important; }
.pb-1, .py-1 { padding-bottom: 0.25rem !important; }
.pl-1, .px-1 { padding-left: 0.25rem !important; }
.p-2 { padding: 0.5rem !important; }
.pt-2, .py-2 { padding-top: 0.5rem !important; }
.pr-2, .px-2 { padding-right: 0.5rem !important; }
.pb-2, .py-2 { padding-bottom: 0.5rem !important; }
.pl-2, .px-2 { padding-left: 0.5rem !important; }
.p-3 { padding: 1rem !important; }
.pt-3, .py-3 { padding-top: 1rem !important; }
.pr-3, .px-3 { padding-right: 1rem !important; }
.pb-3, .py-3 { padding-bottom: 1rem !important; }
.pl-3, .px-3 { padding-left: 1rem !important; }
.p-4 { padding: 1.5rem !important; }
.pt-4, .py-4 { padding-top: 1.5rem !important; }
.pr-4, .px-4 { padding-right: 1.5rem !important; }
.pb-4, .py-4 { padding-bottom: 1.5rem !important; }
.pl-4, .px-4 { padding-left: 1.5rem !important; }
.p-5 { padding: 3rem !important; }
.pt-5, .py-5 { padding-top: 3rem !important; }
.pr-5, .px-5 { padding-right: 3rem !important; }
.pb-5, .py-5 { padding-bottom: 3rem !important; }
.pl-5, .px-5 { padding-left: 3rem !important; }
.m-n1 { margin: -0.25rem !important; }
.mt-n1, .my-n1 { margin-top: -0.25rem !important; }
.mr-n1, .mx-n1 { margin-right: -0.25rem !important; }
.mb-n1, .my-n1 { margin-bottom: -0.25rem !important; }
.ml-n1, .mx-n1 { margin-left: -0.25rem !important; }
.m-n2 { margin: -0.5rem !important; }
.mt-n2, .my-n2 { margin-top: -0.5rem !important; }
.mr-n2, .mx-n2 { margin-right: -0.5rem !important; }
.mb-n2, .my-n2 { margin-bottom: -0.5rem !important; }
.ml-n2, .mx-n2 { margin-left: -0.5rem !important; }
.m-n3 { margin: -1rem !important; }
.mt-n3, .my-n3 { margin-top: -1rem !important; }
.mr-n3, .mx-n3 { margin-right: -1rem !important; }
.mb-n3, .my-n3 { margin-bottom: -1rem !important; }
.ml-n3, .mx-n3 { margin-left: -1rem !important; }
.m-n4 { margin: -1.5rem !important; }
.mt-n4, .my-n4 { margin-top: -1.5rem !important; }
.mr-n4, .mx-n4 { margin-right: -1.5rem !important; }
.mb-n4, .my-n4 { margin-bottom: -1.5rem !important; }
.ml-n4, .mx-n4 { margin-left: -1.5rem !important; }
.m-n5 { margin: -3rem !important; }
.mt-n5, .my-n5 { margin-top: -3rem !important; }
.mr-n5, .mx-n5 { margin-right: -3rem !important; }
.mb-n5, .my-n5 { margin-bottom: -3rem !important; }
.ml-n5, .mx-n5 { margin-left: -3rem !important; }
.m-auto { margin: auto !important; }
.mt-auto, .my-auto { margin-top: auto !important; }
.mr-auto, .mx-auto { margin-right: auto !important; }
.mb-auto, .my-auto { margin-bottom: auto !important; }
.ml-auto, .mx-auto { margin-left: auto !important; }
@media (min-width: 576px) {
  .m-sm-0 { margin: 0px !important; }
  .mt-sm-0, .my-sm-0 { margin-top: 0px !important; }
  .mr-sm-0, .mx-sm-0 { margin-right: 0px !important; }
  .mb-sm-0, .my-sm-0 { margin-bottom: 0px !important; }
  .ml-sm-0, .mx-sm-0 { margin-left: 0px !important; }
  .m-sm-1 { margin: 0.25rem !important; }
  .mt-sm-1, .my-sm-1 { margin-top: 0.25rem !important; }
  .mr-sm-1, .mx-sm-1 { margin-right: 0.25rem !important; }
  .mb-sm-1, .my-sm-1 { margin-bottom: 0.25rem !important; }
  .ml-sm-1, .mx-sm-1 { margin-left: 0.25rem !important; }
  .m-sm-2 { margin: 0.5rem !important; }
  .mt-sm-2, .my-sm-2 { margin-top: 0.5rem !important; }
  .mr-sm-2, .mx-sm-2 { margin-right: 0.5rem !important; }
  .mb-sm-2, .my-sm-2 { margin-bottom: 0.5rem !important; }
  .ml-sm-2, .mx-sm-2 { margin-left: 0.5rem !important; }
  .m-sm-3 { margin: 1rem !important; }
  .mt-sm-3, .my-sm-3 { margin-top: 1rem !important; }
  .mr-sm-3, .mx-sm-3 { margin-right: 1rem !important; }
  .mb-sm-3, .my-sm-3 { margin-bottom: 1rem !important; }
  .ml-sm-3, .mx-sm-3 { margin-left: 1rem !important; }
  .m-sm-4 { margin: 1.5rem !important; }
  .mt-sm-4, .my-sm-4 { margin-top: 1.5rem !important; }
  .mr-sm-4, .mx-sm-4 { margin-right: 1.5rem !important; }
  .mb-sm-4, .my-sm-4 { margin-bottom: 1.5rem !important; }
  .ml-sm-4, .mx-sm-4 { margin-left: 1.5rem !important; }
  .m-sm-5 { margin: 3rem !important; }
  .mt-sm-5, .my-sm-5 { margin-top: 3rem !important; }
  .mr-sm-5, .mx-sm-5 { margin-right: 3rem !important; }
  .mb-sm-5, .my-sm-5 { margin-bottom: 3rem !important; }
  .ml-sm-5, .mx-sm-5 { margin-left: 3rem !important; }
  .p-sm-0 { padding: 0px !important; }
  .pt-sm-0, .py-sm-0 { padding-top: 0px !important; }
  .pr-sm-0, .px-sm-0 { padding-right: 0px !important; }
  .pb-sm-0, .py-sm-0 { padding-bottom: 0px !important; }
  .pl-sm-0, .px-sm-0 { padding-left: 0px !important; }
  .p-sm-1 { padding: 0.25rem !important; }
  .pt-sm-1, .py-sm-1 { padding-top: 0.25rem !important; }
  .pr-sm-1, .px-sm-1 { padding-right: 0.25rem !important; }
  .pb-sm-1, .py-sm-1 { padding-bottom: 0.25rem !important; }
  .pl-sm-1, .px-sm-1 { padding-left: 0.25rem !important; }
  .p-sm-2 { padding: 0.5rem !important; }
  .pt-sm-2, .py-sm-2 { padding-top: 0.5rem !important; }
  .pr-sm-2, .px-sm-2 { padding-right: 0.5rem !important; }
  .pb-sm-2, .py-sm-2 { padding-bottom: 0.5rem !important; }
  .pl-sm-2, .px-sm-2 { padding-left: 0.5rem !important; }
  .p-sm-3 { padding: 1rem !important; }
  .pt-sm-3, .py-sm-3 { padding-top: 1rem !important; }
  .pr-sm-3, .px-sm-3 { padding-right: 1rem !important; }
  .pb-sm-3, .py-sm-3 { padding-bottom: 1rem !important; }
  .pl-sm-3, .px-sm-3 { padding-left: 1rem !important; }
  .p-sm-4 { padding: 1.5rem !important; }
  .pt-sm-4, .py-sm-4 { padding-top: 1.5rem !important; }
  .pr-sm-4, .px-sm-4 { padding-right: 1.5rem !important; }
  .pb-sm-4, .py-sm-4 { padding-bottom: 1.5rem !important; }
  .pl-sm-4, .px-sm-4 { padding-left: 1.5rem !important; }
  .p-sm-5 { padding: 3rem !important; }
  .pt-sm-5, .py-sm-5 { padding-top: 3rem !important; }
  .pr-sm-5, .px-sm-5 { padding-right: 3rem !important; }
  .pb-sm-5, .py-sm-5 { padding-bottom: 3rem !important; }
  .pl-sm-5, .px-sm-5 { padding-left: 3rem !important; }
  .m-sm-n1 { margin: -0.25rem !important; }
  .mt-sm-n1, .my-sm-n1 { margin-top: -0.25rem !important; }
  .mr-sm-n1, .mx-sm-n1 { margin-right: -0.25rem !important; }
  .mb-sm-n1, .my-sm-n1 { margin-bottom: -0.25rem !important; }
  .ml-sm-n1, .mx-sm-n1 { margin-left: -0.25rem !important; }
  .m-sm-n2 { margin: -0.5rem !important; }
  .mt-sm-n2, .my-sm-n2 { margin-top: -0.5rem !important; }
  .mr-sm-n2, .mx-sm-n2 { margin-right: -0.5rem !important; }
  .mb-sm-n2, .my-sm-n2 { margin-bottom: -0.5rem !important; }
  .ml-sm-n2, .mx-sm-n2 { margin-left: -0.5rem !important; }
  .m-sm-n3 { margin: -1rem !important; }
  .mt-sm-n3, .my-sm-n3 { margin-top: -1rem !important; }
  .mr-sm-n3, .mx-sm-n3 { margin-right: -1rem !important; }
  .mb-sm-n3, .my-sm-n3 { margin-bottom: -1rem !important; }
  .ml-sm-n3, .mx-sm-n3 { margin-left: -1rem !important; }
  .m-sm-n4 { margin: -1.5rem !important; }
  .mt-sm-n4, .my-sm-n4 { margin-top: -1.5rem !important; }
  .mr-sm-n4, .mx-sm-n4 { margin-right: -1.5rem !important; }
  .mb-sm-n4, .my-sm-n4 { margin-bottom: -1.5rem !important; }
  .ml-sm-n4, .mx-sm-n4 { margin-left: -1.5rem !important; }
  .m-sm-n5 { margin: -3rem !important; }
  .mt-sm-n5, .my-sm-n5 { margin-top: -3rem !important; }
  .mr-sm-n5, .mx-sm-n5 { margin-right: -3rem !important; }
  .mb-sm-n5, .my-sm-n5 { margin-bottom: -3rem !important; }
  .ml-sm-n5, .mx-sm-n5 { margin-left: -3rem !important; }
  .m-sm-auto { margin: auto !important; }
  .mt-sm-auto, .my-sm-auto { margin-top: auto !important; }
  .mr-sm-auto, .mx-sm-auto { margin-right: auto !important; }
  .mb-sm-auto, .my-sm-auto { margin-bottom: auto !important; }
  .ml-sm-auto, .mx-sm-auto { margin-left: auto !important; }
}
@media (min-width: 768px) {
  .m-md-0 { margin: 0px !important; }
  .mt-md-0, .my-md-0 { margin-top: 0px !important; }
  .mr-md-0, .mx-md-0 { margin-right: 0px !important; }
  .mb-md-0, .my-md-0 { margin-bottom: 0px !important; }
  .ml-md-0, .mx-md-0 { margin-left: 0px !important; }
  .m-md-1 { margin: 0.25rem !important; }
  .mt-md-1, .my-md-1 { margin-top: 0.25rem !important; }
  .mr-md-1, .mx-md-1 { margin-right: 0.25rem !important; }
  .mb-md-1, .my-md-1 { margin-bottom: 0.25rem !important; }
  .ml-md-1, .mx-md-1 { margin-left: 0.25rem !important; }
  .m-md-2 { margin: 0.5rem !important; }
  .mt-md-2, .my-md-2 { margin-top: 0.5rem !important; }
  .mr-md-2, .mx-md-2 { margin-right: 0.5rem !important; }
  .mb-md-2, .my-md-2 { margin-bottom: 0.5rem !important; }
  .ml-md-2, .mx-md-2 { margin-left: 0.5rem !important; }
  .m-md-3 { margin: 1rem !important; }
  .mt-md-3, .my-md-3 { margin-top: 1rem !important; }
  .mr-md-3, .mx-md-3 { margin-right: 1rem !important; }
  .mb-md-3, .my-md-3 { margin-bottom: 1rem !important; }
  .ml-md-3, .mx-md-3 { margin-left: 1rem !important; }
  .m-md-4 { margin: 1.5rem !important; }
  .mt-md-4, .my-md-4 { margin-top: 1.5rem !important; }
  .mr-md-4, .mx-md-4 { margin-right: 1.5rem !important; }
  .mb-md-4, .my-md-4 { margin-bottom: 1.5rem !important; }
  .ml-md-4, .mx-md-4 { margin-left: 1.5rem !important; }
  .m-md-5 { margin: 3rem !important; }
  .mt-md-5, .my-md-5 { margin-top: 3rem !important; }
  .mr-md-5, .mx-md-5 { margin-right: 3rem !important; }
  .mb-md-5, .my-md-5 { margin-bottom: 3rem !important; }
  .ml-md-5, .mx-md-5 { margin-left: 3rem !important; }
  .p-md-0 { padding: 0px !important; }
  .pt-md-0, .py-md-0 { padding-top: 0px !important; }
  .pr-md-0, .px-md-0 { padding-right: 0px !important; }
  .pb-md-0, .py-md-0 { padding-bottom: 0px !important; }
  .pl-md-0, .px-md-0 { padding-left: 0px !important; }
  .p-md-1 { padding: 0.25rem !important; }
  .pt-md-1, .py-md-1 { padding-top: 0.25rem !important; }
  .pr-md-1, .px-md-1 { padding-right: 0.25rem !important; }
  .pb-md-1, .py-md-1 { padding-bottom: 0.25rem !important; }
  .pl-md-1, .px-md-1 { padding-left: 0.25rem !important; }
  .p-md-2 { padding: 0.5rem !important; }
  .pt-md-2, .py-md-2 { padding-top: 0.5rem !important; }
  .pr-md-2, .px-md-2 { padding-right: 0.5rem !important; }
  .pb-md-2, .py-md-2 { padding-bottom: 0.5rem !important; }
  .pl-md-2, .px-md-2 { padding-left: 0.5rem !important; }
  .p-md-3 { padding: 1rem !important; }
  .pt-md-3, .py-md-3 { padding-top: 1rem !important; }
  .pr-md-3, .px-md-3 { padding-right: 1rem !important; }
  .pb-md-3, .py-md-3 { padding-bottom: 1rem !important; }
  .pl-md-3, .px-md-3 { padding-left: 1rem !important; }
  .p-md-4 { padding: 1.5rem !important; }
  .pt-md-4, .py-md-4 { padding-top: 1.5rem !important; }
  .pr-md-4, .px-md-4 { padding-right: 1.5rem !important; }
  .pb-md-4, .py-md-4 { padding-bottom: 1.5rem !important; }
  .pl-md-4, .px-md-4 { padding-left: 1.5rem !important; }
  .p-md-5 { padding: 3rem !important; }
  .pt-md-5, .py-md-5 { padding-top: 3rem !important; }
  .pr-md-5, .px-md-5 { padding-right: 3rem !important; }
  .pb-md-5, .py-md-5 { padding-bottom: 3rem !important; }
  .pl-md-5, .px-md-5 { padding-left: 3rem !important; }
  .m-md-n1 { margin: -0.25rem !important; }
  .mt-md-n1, .my-md-n1 { margin-top: -0.25rem !important; }
  .mr-md-n1, .mx-md-n1 { margin-right: -0.25rem !important; }
  .mb-md-n1, .my-md-n1 { margin-bottom: -0.25rem !important; }
  .ml-md-n1, .mx-md-n1 { margin-left: -0.25rem !important; }
  .m-md-n2 { margin: -0.5rem !important; }
  .mt-md-n2, .my-md-n2 { margin-top: -0.5rem !important; }
  .mr-md-n2, .mx-md-n2 { margin-right: -0.5rem !important; }
  .mb-md-n2, .my-md-n2 { margin-bottom: -0.5rem !important; }
  .ml-md-n2, .mx-md-n2 { margin-left: -0.5rem !important; }
  .m-md-n3 { margin: -1rem !important; }
  .mt-md-n3, .my-md-n3 { margin-top: -1rem !important; }
  .mr-md-n3, .mx-md-n3 { margin-right: -1rem !important; }
  .mb-md-n3, .my-md-n3 { margin-bottom: -1rem !important; }
  .ml-md-n3, .mx-md-n3 { margin-left: -1rem !important; }
  .m-md-n4 { margin: -1.5rem !important; }
  .mt-md-n4, .my-md-n4 { margin-top: -1.5rem !important; }
  .mr-md-n4, .mx-md-n4 { margin-right: -1.5rem !important; }
  .mb-md-n4, .my-md-n4 { margin-bottom: -1.5rem !important; }
  .ml-md-n4, .mx-md-n4 { margin-left: -1.5rem !important; }
  .m-md-n5 { margin: -3rem !important; }
  .mt-md-n5, .my-md-n5 { margin-top: -3rem !important; }
  .mr-md-n5, .mx-md-n5 { margin-right: -3rem !important; }
  .mb-md-n5, .my-md-n5 { margin-bottom: -3rem !important; }
  .ml-md-n5, .mx-md-n5 { margin-left: -3rem !important; }
  .m-md-auto { margin: auto !important; }
  .mt-md-auto, .my-md-auto { margin-top: auto !important; }
  .mr-md-auto, .mx-md-auto { margin-right: auto !important; }
  .mb-md-auto, .my-md-auto { margin-bottom: auto !important; }
  .ml-md-auto, .mx-md-auto { margin-left: auto !important; }
}
@media (min-width: 992px) {
  .m-lg-0 { margin: 0px !important; }
  .mt-lg-0, .my-lg-0 { margin-top: 0px !important; }
  .mr-lg-0, .mx-lg-0 { margin-right: 0px !important; }
  .mb-lg-0, .my-lg-0 { margin-bottom: 0px !important; }
  .ml-lg-0, .mx-lg-0 { margin-left: 0px !important; }
  .m-lg-1 { margin: 0.25rem !important; }
  .mt-lg-1, .my-lg-1 { margin-top: 0.25rem !important; }
  .mr-lg-1, .mx-lg-1 { margin-right: 0.25rem !important; }
  .mb-lg-1, .my-lg-1 { margin-bottom: 0.25rem !important; }
  .ml-lg-1, .mx-lg-1 { margin-left: 0.25rem !important; }
  .m-lg-2 { margin: 0.5rem !important; }
  .mt-lg-2, .my-lg-2 { margin-top: 0.5rem !important; }
  .mr-lg-2, .mx-lg-2 { margin-right: 0.5rem !important; }
  .mb-lg-2, .my-lg-2 { margin-bottom: 0.5rem !important; }
  .ml-lg-2, .mx-lg-2 { margin-left: 0.5rem !important; }
  .m-lg-3 { margin: 1rem !important; }
  .mt-lg-3, .my-lg-3 { margin-top: 1rem !important; }
  .mr-lg-3, .mx-lg-3 { margin-right: 1rem !important; }
  .mb-lg-3, .my-lg-3 { margin-bottom: 1rem !important; }
  .ml-lg-3, .mx-lg-3 { margin-left: 1rem !important; }
  .m-lg-4 { margin: 1.5rem !important; }
  .mt-lg-4, .my-lg-4 { margin-top: 1.5rem !important; }
  .mr-lg-4, .mx-lg-4 { margin-right: 1.5rem !important; }
  .mb-lg-4, .my-lg-4 { margin-bottom: 1.5rem !important; }
  .ml-lg-4, .mx-lg-4 { margin-left: 1.5rem !important; }
  .m-lg-5 { margin: 3rem !important; }
  .mt-lg-5, .my-lg-5 { margin-top: 3rem !important; }
  .mr-lg-5, .mx-lg-5 { margin-right: 3rem !important; }
  .mb-lg-5, .my-lg-5 { margin-bottom: 3rem !important; }
  .ml-lg-5, .mx-lg-5 { margin-left: 3rem !important; }
  .p-lg-0 { padding: 0px !important; }
  .pt-lg-0, .py-lg-0 { padding-top: 0px !important; }
  .pr-lg-0, .px-lg-0 { padding-right: 0px !important; }
  .pb-lg-0, .py-lg-0 { padding-bottom: 0px !important; }
  .pl-lg-0, .px-lg-0 { padding-left: 0px !important; }
  .p-lg-1 { padding: 0.25rem !important; }
  .pt-lg-1, .py-lg-1 { padding-top: 0.25rem !important; }
  .pr-lg-1, .px-lg-1 { padding-right: 0.25rem !important; }
  .pb-lg-1, .py-lg-1 { padding-bottom: 0.25rem !important; }
  .pl-lg-1, .px-lg-1 { padding-left: 0.25rem !important; }
  .p-lg-2 { padding: 0.5rem !important; }
  .pt-lg-2, .py-lg-2 { padding-top: 0.5rem !important; }
  .pr-lg-2, .px-lg-2 { padding-right: 0.5rem !important; }
  .pb-lg-2, .py-lg-2 { padding-bottom: 0.5rem !important; }
  .pl-lg-2, .px-lg-2 { padding-left: 0.5rem !important; }
  .p-lg-3 { padding: 1rem !important; }
  .pt-lg-3, .py-lg-3 { padding-top: 1rem !important; }
  .pr-lg-3, .px-lg-3 { padding-right: 1rem !important; }
  .pb-lg-3, .py-lg-3 { padding-bottom: 1rem !important; }
  .pl-lg-3, .px-lg-3 { padding-left: 1rem !important; }
  .p-lg-4 { padding: 1.5rem !important; }
  .pt-lg-4, .py-lg-4 { padding-top: 1.5rem !important; }
  .pr-lg-4, .px-lg-4 { padding-right: 1.5rem !important; }
  .pb-lg-4, .py-lg-4 { padding-bottom: 1.5rem !important; }
  .pl-lg-4, .px-lg-4 { padding-left: 1.5rem !important; }
  .p-lg-5 { padding: 3rem !important; }
  .pt-lg-5, .py-lg-5 { padding-top: 3rem !important; }
  .pr-lg-5, .px-lg-5 { padding-right: 3rem !important; }
  .pb-lg-5, .py-lg-5 { padding-bottom: 3rem !important; }
  .pl-lg-5, .px-lg-5 { padding-left: 3rem !important; }
  .m-lg-n1 { margin: -0.25rem !important; }
  .mt-lg-n1, .my-lg-n1 { margin-top: -0.25rem !important; }
  .mr-lg-n1, .mx-lg-n1 { margin-right: -0.25rem !important; }
  .mb-lg-n1, .my-lg-n1 { margin-bottom: -0.25rem !important; }
  .ml-lg-n1, .mx-lg-n1 { margin-left: -0.25rem !important; }
  .m-lg-n2 { margin: -0.5rem !important; }
  .mt-lg-n2, .my-lg-n2 { margin-top: -0.5rem !important; }
  .mr-lg-n2, .mx-lg-n2 { margin-right: -0.5rem !important; }
  .mb-lg-n2, .my-lg-n2 { margin-bottom: -0.5rem !important; }
  .ml-lg-n2, .mx-lg-n2 { margin-left: -0.5rem !important; }
  .m-lg-n3 { margin: -1rem !important; }
  .mt-lg-n3, .my-lg-n3 { margin-top: -1rem !important; }
  .mr-lg-n3, .mx-lg-n3 { margin-right: -1rem !important; }
  .mb-lg-n3, .my-lg-n3 { margin-bottom: -1rem !important; }
  .ml-lg-n3, .mx-lg-n3 { margin-left: -1rem !important; }
  .m-lg-n4 { margin: -1.5rem !important; }
  .mt-lg-n4, .my-lg-n4 { margin-top: -1.5rem !important; }
  .mr-lg-n4, .mx-lg-n4 { margin-right: -1.5rem !important; }
  .mb-lg-n4, .my-lg-n4 { margin-bottom: -1.5rem !important; }
  .ml-lg-n4, .mx-lg-n4 { margin-left: -1.5rem !important; }
  .m-lg-n5 { margin: -3rem !important; }
  .mt-lg-n5, .my-lg-n5 { margin-top: -3rem !important; }
  .mr-lg-n5, .mx-lg-n5 { margin-right: -3rem !important; }
  .mb-lg-n5, .my-lg-n5 { margin-bottom: -3rem !important; }
  .ml-lg-n5, .mx-lg-n5 { margin-left: -3rem !important; }
  .m-lg-auto { margin: auto !important; }
  .mt-lg-auto, .my-lg-auto { margin-top: auto !important; }
  .mr-lg-auto, .mx-lg-auto { margin-right: auto !important; }
  .mb-lg-auto, .my-lg-auto { margin-bottom: auto !important; }
  .ml-lg-auto, .mx-lg-auto { margin-left: auto !important; }
}
@media (min-width: 1200px) {
  .m-xl-0 { margin: 0px !important; }
  .mt-xl-0, .my-xl-0 { margin-top: 0px !important; }
  .mr-xl-0, .mx-xl-0 { margin-right: 0px !important; }
  .mb-xl-0, .my-xl-0 { margin-bottom: 0px !important; }
  .ml-xl-0, .mx-xl-0 { margin-left: 0px !important; }
  .m-xl-1 { margin: 0.25rem !important; }
  .mt-xl-1, .my-xl-1 { margin-top: 0.25rem !important; }
  .mr-xl-1, .mx-xl-1 { margin-right: 0.25rem !important; }
  .mb-xl-1, .my-xl-1 { margin-bottom: 0.25rem !important; }
  .ml-xl-1, .mx-xl-1 { margin-left: 0.25rem !important; }
  .m-xl-2 { margin: 0.5rem !important; }
  .mt-xl-2, .my-xl-2 { margin-top: 0.5rem !important; }
  .mr-xl-2, .mx-xl-2 { margin-right: 0.5rem !important; }
  .mb-xl-2, .my-xl-2 { margin-bottom: 0.5rem !important; }
  .ml-xl-2, .mx-xl-2 { margin-left: 0.5rem !important; }
  .m-xl-3 { margin: 1rem !important; }
  .mt-xl-3, .my-xl-3 { margin-top: 1rem !important; }
  .mr-xl-3, .mx-xl-3 { margin-right: 1rem !important; }
  .mb-xl-3, .my-xl-3 { margin-bottom: 1rem !important; }
  .ml-xl-3, .mx-xl-3 { margin-left: 1rem !important; }
  .m-xl-4 { margin: 1.5rem !important; }
  .mt-xl-4, .my-xl-4 { margin-top: 1.5rem !important; }
  .mr-xl-4, .mx-xl-4 { margin-right: 1.5rem !important; }
  .mb-xl-4, .my-xl-4 { margin-bottom: 1.5rem !important; }
  .ml-xl-4, .mx-xl-4 { margin-left: 1.5rem !important; }
  .m-xl-5 { margin: 3rem !important; }
  .mt-xl-5, .my-xl-5 { margin-top: 3rem !important; }
  .mr-xl-5, .mx-xl-5 { margin-right: 3rem !important; }
  .mb-xl-5, .my-xl-5 { margin-bottom: 3rem !important; }
  .ml-xl-5, .mx-xl-5 { margin-left: 3rem !important; }
  .p-xl-0 { padding: 0px !important; }
  .pt-xl-0, .py-xl-0 { padding-top: 0px !important; }
  .pr-xl-0, .px-xl-0 { padding-right: 0px !important; }
  .pb-xl-0, .py-xl-0 { padding-bottom: 0px !important; }
  .pl-xl-0, .px-xl-0 { padding-left: 0px !important; }
  .p-xl-1 { padding: 0.25rem !important; }
  .pt-xl-1, .py-xl-1 { padding-top: 0.25rem !important; }
  .pr-xl-1, .px-xl-1 { padding-right: 0.25rem !important; }
  .pb-xl-1, .py-xl-1 { padding-bottom: 0.25rem !important; }
  .pl-xl-1, .px-xl-1 { padding-left: 0.25rem !important; }
  .p-xl-2 { padding: 0.5rem !important; }
  .pt-xl-2, .py-xl-2 { padding-top: 0.5rem !important; }
  .pr-xl-2, .px-xl-2 { padding-right: 0.5rem !important; }
  .pb-xl-2, .py-xl-2 { padding-bottom: 0.5rem !important; }
  .pl-xl-2, .px-xl-2 { padding-left: 0.5rem !important; }
  .p-xl-3 { padding: 1rem !important; }
  .pt-xl-3, .py-xl-3 { padding-top: 1rem !important; }
  .pr-xl-3, .px-xl-3 { padding-right: 1rem !important; }
  .pb-xl-3, .py-xl-3 { padding-bottom: 1rem !important; }
  .pl-xl-3, .px-xl-3 { padding-left: 1rem !important; }
  .p-xl-4 { padding: 1.5rem !important; }
  .pt-xl-4, .py-xl-4 { padding-top: 1.5rem !important; }
  .pr-xl-4, .px-xl-4 { padding-right: 1.5rem !important; }
  .pb-xl-4, .py-xl-4 { padding-bottom: 1.5rem !important; }
  .pl-xl-4, .px-xl-4 { padding-left: 1.5rem !important; }
  .p-xl-5 { padding: 3rem !important; }
  .pt-xl-5, .py-xl-5 { padding-top: 3rem !important; }
  .pr-xl-5, .px-xl-5 { padding-right: 3rem !important; }
  .pb-xl-5, .py-xl-5 { padding-bottom: 3rem !important; }
  .pl-xl-5, .px-xl-5 { padding-left: 3rem !important; }
  .m-xl-n1 { margin: -0.25rem !important; }
  .mt-xl-n1, .my-xl-n1 { margin-top: -0.25rem !important; }
  .mr-xl-n1, .mx-xl-n1 { margin-right: -0.25rem !important; }
  .mb-xl-n1, .my-xl-n1 { margin-bottom: -0.25rem !important; }
  .ml-xl-n1, .mx-xl-n1 { margin-left: -0.25rem !important; }
  .m-xl-n2 { margin: -0.5rem !important; }
  .mt-xl-n2, .my-xl-n2 { margin-top: -0.5rem !important; }
  .mr-xl-n2, .mx-xl-n2 { margin-right: -0.5rem !important; }
  .mb-xl-n2, .my-xl-n2 { margin-bottom: -0.5rem !important; }
  .ml-xl-n2, .mx-xl-n2 { margin-left: -0.5rem !important; }
  .m-xl-n3 { margin: -1rem !important; }
  .mt-xl-n3, .my-xl-n3 { margin-top: -1rem !important; }
  .mr-xl-n3, .mx-xl-n3 { margin-right: -1rem !important; }
  .mb-xl-n3, .my-xl-n3 { margin-bottom: -1rem !important; }
  .ml-xl-n3, .mx-xl-n3 { margin-left: -1rem !important; }
  .m-xl-n4 { margin: -1.5rem !important; }
  .mt-xl-n4, .my-xl-n4 { margin-top: -1.5rem !important; }
  .mr-xl-n4, .mx-xl-n4 { margin-right: -1.5rem !important; }
  .mb-xl-n4, .my-xl-n4 { margin-bottom: -1.5rem !important; }
  .ml-xl-n4, .mx-xl-n4 { margin-left: -1.5rem !important; }
  .m-xl-n5 { margin: -3rem !important; }
  .mt-xl-n5, .my-xl-n5 { margin-top: -3rem !important; }
  .mr-xl-n5, .mx-xl-n5 { margin-right: -3rem !important; }
  .mb-xl-n5, .my-xl-n5 { margin-bottom: -3rem !important; }
  .ml-xl-n5, .mx-xl-n5 { margin-left: -3rem !important; }
  .m-xl-auto { margin: auto !important; }
  .mt-xl-auto, .my-xl-auto { margin-top: auto !important; }
  .mr-xl-auto, .mx-xl-auto { margin-right: auto !important; }
  .mb-xl-auto, .my-xl-auto { margin-bottom: auto !important; }
  .ml-xl-auto, .mx-xl-auto { margin-left: auto !important; }
}
.stretched-link::after { position: absolute; inset: 0px; z-index: 1; pointer-events: auto; content: ""; background-color: rgba(0, 0, 0, 0); }
.text-monospace { font-family: SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace !important; }
.text-justify { text-align: justify !important; }
.text-wrap { white-space: normal !important; }
.text-nowrap { white-space: nowrap !important; }
.text-truncate { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.text-left { text-align: left !important; }
.text-right { text-align: right !important; }
.text-center { text-align: center !important; }
@media (min-width: 576px) {
  .text-sm-left { text-align: left !important; }
  .text-sm-right { text-align: right !important; }
  .text-sm-center { text-align: center !important; }
}
@media (min-width: 768px) {
  .text-md-left { text-align: left !important; }
  .text-md-right { text-align: right !important; }
  .text-md-center { text-align: center !important; }
}
@media (min-width: 992px) {
  .text-lg-left { text-align: left !important; }
  .text-lg-right { text-align: right !important; }
  .text-lg-center { text-align: center !important; }
}
@media (min-width: 1200px) {
  .text-xl-left { text-align: left !important; }
  .text-xl-right { text-align: right !important; }
  .text-xl-center { text-align: center !important; }
}
.text-lowercase { text-transform: lowercase !important; }
.dropdown .dropdown-menu .dropdown-header, .sidebar .sidebar-heading, .text-uppercase { text-transform: uppercase !important; }
.text-capitalize { text-transform: capitalize !important; }
.font-weight-light { font-weight: 300 !important; }
.font-weight-lighter { font-weight: lighter !important; }
.font-weight-normal { font-weight: 400 !important; }
.font-weight-bold { font-weight: 700 !important; }
.font-weight-bolder { font-weight: bolder !important; }
.font-italic { font-style: italic !important; }
.text-white { color: rgb(255, 255, 255) !important; }
.text-primary { color: rgb(78, 115, 223) !important; }
a.text-primary:focus, a.text-primary:hover { color: rgb(34, 74, 190) !important; }
.text-secondary { color: rgb(133, 135, 150) !important; }
a.text-secondary:focus, a.text-secondary:hover { color: rgb(96, 97, 111) !important; }
.text-success { color: rgb(28, 200, 138) !important; }
a.text-success:focus, a.text-success:hover { color: rgb(19, 133, 92) !important; }
.text-info { color: rgb(54, 185, 204) !important; }
a.text-info:focus, a.text-info:hover { color: rgb(37, 131, 145) !important; }
.text-warning { color: rgb(246, 194, 62) !important; }
a.text-warning:focus, a.text-warning:hover { color: rgb(221, 162, 10) !important; }
.text-danger { color: rgb(231, 74, 59) !important; }
a.text-danger:focus, a.text-danger:hover { color: rgb(190, 38, 23) !important; }
.text-light { color: rgb(248, 249, 252) !important; }
a.text-light:focus, a.text-light:hover { color: rgb(194, 203, 229) !important; }
.text-dark { color: rgb(90, 92, 105) !important; }
a.text-dark:focus, a.text-dark:hover { color: rgb(55, 56, 64) !important; }
.text-body { color: rgb(133, 135, 150) !important; }
.text-muted { color: rgb(133, 135, 150) !important; }
.text-black-50 { color: rgba(0, 0, 0, 0.5) !important; }
.text-white-50 { color: rgba(255, 255, 255, 0.5) !important; }
.text-hide { font: 0px / 0 a; color: transparent; text-shadow: none; background-color: transparent; border: 0px; }
.text-decoration-none { text-decoration: none !important; }
.text-break { word-break: break-word !important; overflow-wrap: break-word !important; }
.text-reset { color: inherit !important; }
.visible { visibility: visible !important; }
.invisible { visibility: hidden !important; }
@media print {
  *, ::after, ::before { text-shadow: none !important; box-shadow: none !important; }
  a:not(.btn) { text-decoration: underline; }
  abbr[title]::after { content: " (" attr(title) ")"; }
  pre { white-space: pre-wrap !important; }
  blockquote, pre { border: 1px solid rgb(183, 185, 204); break-inside: avoid; }
  thead { display: table-header-group; }
  img, tr { break-inside: avoid; }
  h2, h3, p { orphans: 3; widows: 3; }
  h2, h3 { break-after: avoid; }
  @page { size: a3; }
  body { min-width: 992px !important; }
  .container { min-width: 992px !important; }
  .navbar { display: none; }
  .badge { border: 1px solid rgb(0, 0, 0); }
  .table { border-collapse: collapse !important; }
  .table td, .table th { background-color: rgb(255, 255, 255) !important; }
  .table-bordered td, .table-bordered th { border: 1px solid rgb(221, 223, 235) !important; }
  .table-dark { color: inherit; }
  .table-dark tbody + tbody, .table-dark td, .table-dark th, .table-dark thead th { border-color: rgb(227, 230, 240); }
  .table .thead-dark th { color: inherit; border-color: rgb(227, 230, 240); }
}
html { position: relative; min-height: 100%; }
body { height: 100%; }
a:focus { outline: 0px; }
#wrapper { display: flex; }
#wrapper #content-wrapper { background-color: rgb(248, 249, 252); width: 100%; overflow-x: hidden; }
#wrapper #content-wrapper #content { flex: 1 0 auto; }
.container, .container-fluid, .container-lg, .container-md, .container-sm, .container-xl { padding-left: 1.5rem; padding-right: 1.5rem; }
.scroll-to-top { position: fixed; right: 1rem; bottom: 1rem; display: none; width: 2.75rem; height: 2.75rem; text-align: center; color: rgb(255, 255, 255); background: rgba(90, 92, 105, 0.5); line-height: 46px; }
.scroll-to-top:focus, .scroll-to-top:hover { color: rgb(255, 255, 255); }
.scroll-to-top:hover { background: rgb(90, 92, 105); }
.scroll-to-top i { font-weight: 800; }
@-webkit-keyframes growIn { 
  0% { transform: scale(0.9); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
@keyframes growIn { 
  0% { transform: scale(0.9); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
.animated--grow-in, .sidebar .nav-item .collapse { animation-name: growIn; animation-duration: 0.2s; }
@-webkit-keyframes fadeIn { 
  0% { opacity: 0; }
  100% { opacity: 1; }
}
@keyframes fadeIn { 
  0% { opacity: 0; }
  100% { opacity: 1; }
}
.animated--fade-in { animation-name: fadeIn; animation-duration: 0.2s; }
.bg-gradient-primary { background-color: rgb(78, 115, 223); background-image: linear-gradient(rgb(78, 115, 223) 10%, rgb(34, 74, 190) 100%); background-size: cover; }
.bg-gradient-secondary { background-color: rgb(133, 135, 150); background-image: linear-gradient(rgb(133, 135, 150) 10%, rgb(96, 97, 111) 100%); background-size: cover; }
.bg-gradient-success { background-color: rgb(28, 200, 138); background-image: linear-gradient(rgb(28, 200, 138) 10%, rgb(19, 133, 92) 100%); background-size: cover; }
.bg-gradient-info { background-color: rgb(54, 185, 204); background-image: linear-gradient(rgb(54, 185, 204) 10%, rgb(37, 131, 145) 100%); background-size: cover; }
.bg-gradient-warning { background-color: rgb(246, 194, 62); background-image: linear-gradient(rgb(246, 194, 62) 10%, rgb(221, 162, 10) 100%); background-size: cover; }
.bg-gradient-danger { background-color: rgb(231, 74, 59); background-image: linear-gradient(rgb(231, 74, 59) 10%, rgb(190, 38, 23) 100%); background-size: cover; }
.bg-gradient-light { background-color: rgb(248, 249, 252); background-image: linear-gradient(rgb(248, 249, 252) 10%, rgb(194, 203, 229) 100%); background-size: cover; }
.bg-gradient-dark { background-color: rgb(90, 92, 105); background-image: linear-gradient(rgb(90, 92, 105) 10%, rgb(55, 56, 64) 100%); background-size: cover; }
.bg-gray-100 { background-color: rgb(248, 249, 252) !important; }
.bg-gray-200 { background-color: rgb(234, 236, 244) !important; }
.bg-gray-300 { background-color: rgb(221, 223, 235) !important; }
.bg-gray-400 { background-color: rgb(209, 211, 226) !important; }
.bg-gray-500 { background-color: rgb(183, 185, 204) !important; }
.bg-gray-600 { background-color: rgb(133, 135, 150) !important; }
.bg-gray-700 { background-color: rgb(110, 112, 126) !important; }
.bg-gray-800 { background-color: rgb(90, 92, 105) !important; }
.bg-gray-900 { background-color: rgb(58, 59, 69) !important; }
.o-hidden { overflow: hidden !important; }
.text-xs { font-size: 0.7rem; }
.text-lg { font-size: 1.2rem; }
.text-gray-100 { color: rgb(248, 249, 252) !important; }
.text-gray-200 { color: rgb(234, 236, 244) !important; }
.text-gray-300 { color: rgb(221, 223, 235) !important; }
.text-gray-400 { color: rgb(209, 211, 226) !important; }
.text-gray-500 { color: rgb(183, 185, 204) !important; }
.text-gray-600 { color: rgb(133, 135, 150) !important; }
.text-gray-700 { color: rgb(110, 112, 126) !important; }
.text-gray-800 { color: rgb(90, 92, 105) !important; }
.text-gray-900 { color: rgb(58, 59, 69) !important; }
.icon-circle { height: 2.5rem; width: 2.5rem; border-radius: 100%; display: flex; align-items: center; justify-content: center; }
.border-left-primary { border-left: 0.25rem solid rgb(78, 115, 223) !important; }
.border-bottom-primary { border-bottom: 0.25rem solid rgb(78, 115, 223) !important; }
.border-left-secondary { border-left: 0.25rem solid rgb(133, 135, 150) !important; }
.border-bottom-secondary { border-bottom: 0.25rem solid rgb(133, 135, 150) !important; }
.border-left-success { border-left: 0.25rem solid rgb(28, 200, 138) !important; }
.border-bottom-success { border-bottom: 0.25rem solid rgb(28, 200, 138) !important; }
.border-left-info { border-left: 0.25rem solid rgb(54, 185, 204) !important; }
.border-bottom-info { border-bottom: 0.25rem solid rgb(54, 185, 204) !important; }
.border-left-warning { border-left: 0.25rem solid rgb(246, 194, 62) !important; }
.border-bottom-warning { border-bottom: 0.25rem solid rgb(246, 194, 62) !important; }
.border-left-danger { border-left: 0.25rem solid rgb(231, 74, 59) !important; }
.border-bottom-danger { border-bottom: 0.25rem solid rgb(231, 74, 59) !important; }
.border-left-light { border-left: 0.25rem solid rgb(248, 249, 252) !important; }
.border-bottom-light { border-bottom: 0.25rem solid rgb(248, 249, 252) !important; }
.border-left-dark { border-left: 0.25rem solid rgb(90, 92, 105) !important; }
.border-bottom-dark { border-bottom: 0.25rem solid rgb(90, 92, 105) !important; }
.progress-sm { height: 0.5rem; }
.rotate-15 { transform: rotate(15deg); }
.rotate-n-15 { transform: rotate(-15deg); }
.dropdown .dropdown-menu { font-size: 0.85rem; }
.dropdown .dropdown-menu .dropdown-header { font-weight: 800; font-size: 0.65rem; color: rgb(183, 185, 204); }
.dropdown.no-arrow .dropdown-toggle::after { display: none; }
.sidebar .nav-item.dropdown .dropdown-toggle::after, .topbar .nav-item.dropdown .dropdown-toggle::after { width: 1rem; text-align: center; float: right; vertical-align: 0px; border: 0px; font-weight: 900; content: ""; font-family: "Font Awesome 5 Free"; }
.sidebar .nav-item.dropdown.show .dropdown-toggle::after, .topbar .nav-item.dropdown.show .dropdown-toggle::after { content: ""; }
.sidebar .nav-item .nav-link, .topbar .nav-item .nav-link { position: relative; }
.sidebar .nav-item .nav-link .badge-counter, .topbar .nav-item .nav-link .badge-counter { position: absolute; transform: scale(0.7); transform-origin: right top; right: 0.25rem; margin-top: -0.25rem; }
.sidebar .nav-item .nav-link .img-profile, .topbar .nav-item .nav-link .img-profile { height: 2rem; width: 2rem; }
.topbar { height: 4.375rem; }
.topbar #sidebarToggleTop { height: 2.5rem; width: 2.5rem; }
.topbar #sidebarToggleTop:hover { background-color: rgb(234, 236, 244); }
.topbar #sidebarToggleTop:active { background-color: rgb(221, 223, 235); }
.topbar .navbar-search { width: 25rem; }
.topbar .navbar-search input { font-size: 0.85rem; height: auto; }
.topbar .topbar-divider { width: 0px; border-right: 1px solid rgb(227, 230, 240); height: calc(2.375rem); margin: auto 1rem; }
.topbar .nav-item .nav-link { height: 4.375rem; display: flex; align-items: center; padding: 0px 0.75rem; }
.topbar .nav-item .nav-link:focus { outline: 0px; }
.topbar .nav-item:focus { outline: 0px; }
.topbar .dropdown { position: static; }
.topbar .dropdown .dropdown-menu { width: calc(100% - 1.5rem); right: 0.75rem; }
.topbar .dropdown-list { padding: 0px; border: none; overflow: hidden; }
.topbar .dropdown-list .dropdown-header { background-color: rgb(78, 115, 223); border: 1px solid rgb(78, 115, 223); padding-top: 0.75rem; padding-bottom: 0.75rem; color: rgb(255, 255, 255); }
.topbar .dropdown-list .dropdown-item { white-space: normal; padding-top: 0.5rem; padding-bottom: 0.5rem; border-left: 1px solid rgb(227, 230, 240); border-right: 1px solid rgb(227, 230, 240); border-bottom: 1px solid rgb(227, 230, 240); line-height: 1.3rem; }
.topbar .dropdown-list .dropdown-item .dropdown-list-image { position: relative; height: 2.5rem; width: 2.5rem; }
.topbar .dropdown-list .dropdown-item .dropdown-list-image img { height: 2.5rem; width: 2.5rem; }
.topbar .dropdown-list .dropdown-item .dropdown-list-image .status-indicator { background-color: rgb(234, 236, 244); height: 0.75rem; width: 0.75rem; border-radius: 100%; position: absolute; bottom: 0px; right: 0px; border: 0.125rem solid rgb(255, 255, 255); }
.topbar .dropdown-list .dropdown-item .text-truncate { max-width: 10rem; }
.topbar .dropdown-list .dropdown-item:active { background-color: rgb(234, 236, 244); color: rgb(58, 59, 69); }
@media (min-width: 576px) {
  .topbar .dropdown { position: relative; }
  .topbar .dropdown .dropdown-menu { width: auto; right: 0px; }
  .topbar .dropdown-list { width: 20rem !important; }
  .topbar .dropdown-list .dropdown-item .text-truncate { max-width: 13.375rem; }
}
.topbar.navbar-dark .navbar-nav .nav-item .nav-link { color: rgba(255, 255, 255, 0.8); }
.topbar.navbar-dark .navbar-nav .nav-item .nav-link:hover { color: rgb(255, 255, 255); }
.topbar.navbar-dark .navbar-nav .nav-item .nav-link:active { color: rgb(255, 255, 255); }
.topbar.navbar-light .navbar-nav .nav-item .nav-link { color: rgb(209, 211, 226); }
.topbar.navbar-light .navbar-nav .nav-item .nav-link:hover { color: rgb(183, 185, 204); }
.topbar.navbar-light .navbar-nav .nav-item .nav-link:active { color: rgb(133, 135, 150); }
.sidebar { width: 6.5rem; min-height: 100vh; }
.sidebar .nav-item { position: relative; }
.sidebar .nav-item:last-child { margin-bottom: 1rem; }
.sidebar .nav-item .nav-link { text-align: center; padding: 0.75rem 1rem; width: 6.5rem; }
.sidebar .nav-item .nav-link span { font-size: 0.65rem; display: block; }
.sidebar .nav-item.active .nav-link { font-weight: 700; }
.sidebar .nav-item .collapse { position: absolute; left: calc(7.25rem); z-index: 1; top: 2px; }
.sidebar .nav-item .collapse .collapse-inner { border-radius: 0.35rem; box-shadow: rgba(58, 59, 69, 0.15) 0px 0.15rem 1.75rem 0px; }
.sidebar .nav-item .collapsing { display: none; transition: none 0s ease 0s; }
.sidebar .nav-item .collapse .collapse-inner, .sidebar .nav-item .collapsing .collapse-inner { padding: 0.5rem 0px; min-width: 10rem; font-size: 0.85rem; margin: 0px 0px 1rem; }
.sidebar .nav-item .collapse .collapse-inner .collapse-header, .sidebar .nav-item .collapsing .collapse-inner .collapse-header { margin: 0px; white-space: nowrap; padding: 0.5rem 1.5rem; text-transform: uppercase; font-weight: 800; font-size: 0.65rem; color: rgb(183, 185, 204); }
.sidebar .nav-item .collapse .collapse-inner .collapse-item, .sidebar .nav-item .collapsing .collapse-inner .collapse-item { padding: 0.5rem 1rem; margin: 0px 0.5rem; display: block; color: rgb(58, 59, 69); text-decoration: none; border-radius: 0.35rem; white-space: nowrap; }
.sidebar .nav-item .collapse .collapse-inner .collapse-item:hover, .sidebar .nav-item .collapsing .collapse-inner .collapse-item:hover { background-color: rgb(234, 236, 244); }
.sidebar .nav-item .collapse .collapse-inner .collapse-item:active, .sidebar .nav-item .collapsing .collapse-inner .collapse-item:active { background-color: rgb(221, 223, 235); }
.sidebar .nav-item .collapse .collapse-inner .collapse-item.active, .sidebar .nav-item .collapsing .collapse-inner .collapse-item.active { color: rgb(78, 115, 223); font-weight: 700; }
.sidebar #sidebarToggle { width: 2.5rem; height: 2.5rem; text-align: center; margin-bottom: 1rem; cursor: pointer; }
.sidebar #sidebarToggle::after { font-weight: 900; content: ""; font-family: "Font Awesome 5 Free"; margin-right: 0.1rem; }
.sidebar #sidebarToggle:hover { text-decoration: none; }
.sidebar #sidebarToggle:focus { outline: 0px; }
.sidebar.toggled { overflow: hidden; width: 0px !important; }
.sidebar.toggled #sidebarToggle::after { content: ""; font-family: "Font Awesome 5 Free"; margin-left: 0.25rem; }
.sidebar.toggled .sidebar-card { display: none; }
.sidebar .sidebar-brand { height: 4.375rem; text-decoration: none; font-size: 1rem; font-weight: 800; padding: 1.5rem 1rem; text-align: center; text-transform: uppercase; letter-spacing: 0.05rem; z-index: 1; }
.sidebar .sidebar-brand .sidebar-brand-icon i { font-size: 2rem; }
.sidebar .sidebar-brand .sidebar-brand-text { display: none; }
.sidebar hr.sidebar-divider { margin: 0px 1rem 1rem; }
.sidebar .sidebar-heading { text-align: center; padding: 0px 1rem; font-weight: 800; font-size: 0.65rem; }
.sidebar .sidebar-card { display: flex; flex-direction: column; align-items: center; font-size: 0.875rem; border-radius: 0.35rem; color: rgba(255, 255, 255, 0.8); margin-left: 1rem; margin-right: 1rem; margin-bottom: 1rem; padding: 1rem; background-color: rgba(0, 0, 0, 0.1); }
.sidebar .sidebar-card .sidebar-card-illustration { height: 3rem; display: block; }
.sidebar .sidebar-card .sidebar-card-title { font-weight: 700; }
.sidebar .sidebar-card p { font-size: 0.75rem; color: rgba(255, 255, 255, 0.5); }
@media (min-width: 768px) {
  .sidebar { width: 14rem !important; }
  .sidebar .nav-item .collapse { position: relative; left: 0px; z-index: 1; top: 0px; animation: auto ease 0s 1 normal none running none; }
  .sidebar .nav-item .collapse .collapse-inner { border-radius: 0px; box-shadow: none; }
  .sidebar .nav-item .collapsing { display: block; transition: height 0.15s ease 0s; }
  .sidebar .nav-item .collapse, .sidebar .nav-item .collapsing { margin: 0px 1rem; }
  .sidebar .nav-item .nav-link { display: block; text-align: left; padding: 1rem; width: 14rem; }
  .sidebar .nav-item .nav-link i { font-size: 0.85rem; margin-right: 0.25rem; }
  .sidebar .nav-item .nav-link span { font-size: 0.85rem; display: inline; }
  .sidebar .nav-item .nav-link[data-toggle="collapse"]::after { width: 1rem; text-align: center; float: right; vertical-align: 0px; border: 0px; font-weight: 900; content: ""; font-family: "Font Awesome 5 Free"; }
  .sidebar .nav-item .nav-link[data-toggle="collapse"].collapsed::after { content: ""; }
  .sidebar .sidebar-brand .sidebar-brand-icon i { font-size: 2rem; }
  .sidebar .sidebar-brand .sidebar-brand-text { display: inline; }
  .sidebar .sidebar-heading { text-align: left; }
  .sidebar.toggled { overflow: visible; width: 6.5rem !important; }
  .sidebar.toggled .nav-item .collapse { position: absolute; left: calc(7.25rem); z-index: 1; top: 2px; animation-name: growIn; animation-duration: 0.2s; }
  .sidebar.toggled .nav-item .collapse .collapse-inner { box-shadow: rgba(58, 59, 69, 0.15) 0px 0.15rem 1.75rem 0px; border-radius: 0.35rem; }
  .sidebar.toggled .nav-item .collapsing { display: none; transition: none 0s ease 0s; }
  .sidebar.toggled .nav-item .collapse, .sidebar.toggled .nav-item .collapsing { margin: 0px; }
  .sidebar.toggled .nav-item:last-child { margin-bottom: 1rem; }
  .sidebar.toggled .nav-item .nav-link { text-align: center; padding: 0.75rem 1rem; width: 6.5rem; }
  .sidebar.toggled .nav-item .nav-link span { font-size: 0.65rem; display: block; }
  .sidebar.toggled .nav-item .nav-link i { margin-right: 0px; }
  .sidebar.toggled .nav-item .nav-link[data-toggle="collapse"]::after { display: none; }
  .sidebar.toggled .sidebar-brand .sidebar-brand-icon i { font-size: 2rem; }
  .sidebar.toggled .sidebar-brand .sidebar-brand-text { display: none; }
  .sidebar.toggled .sidebar-heading { text-align: center; }
}
.sidebar-light .sidebar-brand { color: rgb(110, 112, 126); }
.sidebar-light hr.sidebar-divider { border-top: 1px solid rgb(234, 236, 244); }
.sidebar-light .sidebar-heading { color: rgb(183, 185, 204); }
.sidebar-light .nav-item .nav-link { color: rgb(133, 135, 150); }
.sidebar-light .nav-item .nav-link i { color: rgb(209, 211, 226); }
.sidebar-light .nav-item .nav-link:active, .sidebar-light .nav-item .nav-link:focus, .sidebar-light .nav-item .nav-link:hover { color: rgb(110, 112, 126); }
.sidebar-light .nav-item .nav-link:active i, .sidebar-light .nav-item .nav-link:focus i, .sidebar-light .nav-item .nav-link:hover i { color: rgb(110, 112, 126); }
.sidebar-light .nav-item .nav-link[data-toggle="collapse"]::after { color: rgb(183, 185, 204); }
.sidebar-light .nav-item.active .nav-link { color: rgb(110, 112, 126); }
.sidebar-light .nav-item.active .nav-link i { color: rgb(110, 112, 126); }
.sidebar-light #sidebarToggle { background-color: rgb(234, 236, 244); }
.sidebar-light #sidebarToggle::after { color: rgb(183, 185, 204); }
.sidebar-light #sidebarToggle:hover { background-color: rgb(221, 223, 235); }
.sidebar-dark .sidebar-brand { color: rgb(255, 255, 255); }
.sidebar-dark hr.sidebar-divider { border-top: 1px solid rgba(255, 255, 255, 0.15); }
.sidebar-dark .sidebar-heading { color: rgba(255, 255, 255, 0.4); }
.sidebar-dark .nav-item .nav-link { color: rgba(255, 255, 255, 0.8); }
.sidebar-dark .nav-item .nav-link i { color: rgba(255, 255, 255, 0.3); }
.sidebar-dark .nav-item .nav-link:active, .sidebar-dark .nav-item .nav-link:focus, .sidebar-dark .nav-item .nav-link:hover { color: rgb(255, 255, 255); }
.sidebar-dark .nav-item .nav-link:active i, .sidebar-dark .nav-item .nav-link:focus i, .sidebar-dark .nav-item .nav-link:hover i { color: rgb(255, 255, 255); }
.sidebar-dark .nav-item .nav-link[data-toggle="collapse"]::after { color: rgba(255, 255, 255, 0.5); }
.sidebar-dark .nav-item.active .nav-link { color: rgb(255, 255, 255); }
.sidebar-dark .nav-item.active .nav-link i { color: rgb(255, 255, 255); }
.sidebar-dark #sidebarToggle { background-color: rgba(255, 255, 255, 0.2); }
.sidebar-dark #sidebarToggle::after { color: rgba(255, 255, 255, 0.5); }
.sidebar-dark #sidebarToggle:hover { background-color: rgba(255, 255, 255, 0.25); }
.sidebar-dark.toggled #sidebarToggle::after { color: rgba(255, 255, 255, 0.5); }
.btn-circle { border-radius: 100%; height: 2.5rem; width: 2.5rem; font-size: 1rem; display: inline-flex; align-items: center; justify-content: center; }
.btn-circle.btn-sm, .btn-group-sm > .btn-circle.btn { height: 1.8rem; width: 1.8rem; font-size: 0.75rem; }
.btn-circle.btn-lg, .btn-group-lg > .btn-circle.btn { height: 3.5rem; width: 3.5rem; font-size: 1.35rem; }
.btn-icon-split { padding: 0px; overflow: hidden; display: inline-flex; align-items: stretch; justify-content: center; }
.btn-icon-split .icon { background: rgba(0, 0, 0, 0.15); display: inline-block; padding: 0.375rem 0.75rem; }
.btn-icon-split .text { display: inline-block; padding: 0.375rem 0.75rem; }
.btn-group-sm > .btn-icon-split.btn .icon, .btn-icon-split.btn-sm .icon { padding: 0.25rem 0.5rem; }
.btn-group-sm > .btn-icon-split.btn .text, .btn-icon-split.btn-sm .text { padding: 0.25rem 0.5rem; }
.btn-group-lg > .btn-icon-split.btn .icon, .btn-icon-split.btn-lg .icon { padding: 0.5rem 1rem; }
.btn-group-lg > .btn-icon-split.btn .text, .btn-icon-split.btn-lg .text { padding: 0.5rem 1rem; }
.card .card-header .dropdown { line-height: 1; }
.card .card-header .dropdown .dropdown-menu { line-height: 1.5; }
.card .card-header[data-toggle="collapse"] { text-decoration: none; position: relative; padding: 0.75rem 3.25rem 0.75rem 1.25rem; }
.card .card-header[data-toggle="collapse"]::after { position: absolute; right: 0px; top: 0px; padding-right: 1.725rem; line-height: 51px; font-weight: 900; content: ""; font-family: "Font Awesome 5 Free"; color: rgb(209, 211, 226); }
.card .card-header[data-toggle="collapse"].collapsed { border-radius: 0.35rem; }
.card .card-header[data-toggle="collapse"].collapsed::after { content: ""; }
.chart-area { position: relative; height: 10rem; width: 100%; }
@media (min-width: 768px) {
  .chart-area { height: 20rem; }
}
.chart-bar { position: relative; height: 10rem; width: 100%; }
@media (min-width: 768px) {
  .chart-bar { height: 20rem; }
}
.chart-pie { position: relative; height: 15rem; width: 100%; }
@media (min-width: 768px) {
  .chart-pie { height: calc(20rem - 43px) !important; }
}
.bg-login-image { background: url("https://source.unsplash.com/K4mSJ7kc0As/600x800") center center / cover; }
.bg-register-image { background: url("https://source.unsplash.com/Mv9hjnEUHR4/600x800") center center / cover; }
.bg-password-image { background: url("https://source.unsplash.com/oWTW-jNGl9I/600x800") center center / cover; }
form.user .custom-checkbox.small label { line-height: 1.5rem; }
form.user .form-control-user { font-size: 0.8rem; border-radius: 10rem; padding: 1.5rem 1rem; }
form.user .btn-user { font-size: 0.8rem; border-radius: 10rem; padding: 0.75rem 1rem; }
.btn-google { color: rgb(255, 255, 255); background-color: rgb(234, 67, 53); border-color: rgb(255, 255, 255); }
.btn-google:hover { color: rgb(255, 255, 255); background-color: rgb(225, 39, 23); border-color: rgb(230, 230, 230); }
.btn-google.focus, .btn-google:focus { color: rgb(255, 255, 255); background-color: rgb(225, 39, 23); border-color: rgb(230, 230, 230); box-shadow: rgba(255, 255, 255, 0.5) 0px 0px 0px 0.2rem; }
.btn-google.disabled, .btn-google:disabled { color: rgb(255, 255, 255); background-color: rgb(234, 67, 53); border-color: rgb(255, 255, 255); }
.btn-google:not(:disabled):not(.disabled).active, .btn-google:not(:disabled):not(.disabled):active, .show > .btn-google.dropdown-toggle { color: rgb(255, 255, 255); background-color: rgb(214, 37, 22); border-color: rgb(223, 223, 223); }
.btn-google:not(:disabled):not(.disabled).active:focus, .btn-google:not(:disabled):not(.disabled):active:focus, .show > .btn-google.dropdown-toggle:focus { box-shadow: rgba(255, 255, 255, 0.5) 0px 0px 0px 0.2rem; }
.btn-facebook { color: rgb(255, 255, 255); background-color: rgb(59, 89, 152); border-color: rgb(255, 255, 255); }
.btn-facebook:hover { color: rgb(255, 255, 255); background-color: rgb(48, 73, 124); border-color: rgb(230, 230, 230); }
.btn-facebook.focus, .btn-facebook:focus { color: rgb(255, 255, 255); background-color: rgb(48, 73, 124); border-color: rgb(230, 230, 230); box-shadow: rgba(255, 255, 255, 0.5) 0px 0px 0px 0.2rem; }
.btn-facebook.disabled, .btn-facebook:disabled { color: rgb(255, 255, 255); background-color: rgb(59, 89, 152); border-color: rgb(255, 255, 255); }
.btn-facebook:not(:disabled):not(.disabled).active, .btn-facebook:not(:disabled):not(.disabled):active, .show > .btn-facebook.dropdown-toggle { color: rgb(255, 255, 255); background-color: rgb(45, 67, 115); border-color: rgb(223, 223, 223); }
.btn-facebook:not(:disabled):not(.disabled).active:focus, .btn-facebook:not(:disabled):not(.disabled):active:focus, .show > .btn-facebook.dropdown-toggle:focus { box-shadow: rgba(255, 255, 255, 0.5) 0px 0px 0px 0.2rem; }
.error { color: rgb(90, 92, 105); font-size: 7rem; position: relative; line-height: 1; width: 12.5rem; }
@-webkit-keyframes noise-anim { 
  0% { clip: rect(81px, 9999px, 74px, 0px); }
  5% { clip: rect(2px, 9999px, 29px, 0px); }
  10% { clip: rect(1px, 9999px, 15px, 0px); }
  15% { clip: rect(50px, 9999px, 8px, 0px); }
  20% { clip: rect(99px, 9999px, 79px, 0px); }
  25% { clip: rect(85px, 9999px, 15px, 0px); }
  30% { clip: rect(41px, 9999px, 53px, 0px); }
  35% { clip: rect(22px, 9999px, 36px, 0px); }
  40% { clip: rect(73px, 9999px, 79px, 0px); }
  45% { clip: rect(82px, 9999px, 100px, 0px); }
  50% { clip: rect(47px, 9999px, 96px, 0px); }
  55% { clip: rect(10px, 9999px, 44px, 0px); }
  60% { clip: rect(7px, 9999px, 24px, 0px); }
  65% { clip: rect(29px, 9999px, 88px, 0px); }
  70% { clip: rect(12px, 9999px, 44px, 0px); }
  75% { clip: rect(25px, 9999px, 57px, 0px); }
  80% { clip: rect(38px, 9999px, 35px, 0px); }
  85% { clip: rect(20px, 9999px, 96px, 0px); }
  90% { clip: rect(58px, 9999px, 44px, 0px); }
  95% { clip: rect(72px, 9999px, 41px, 0px); }
  100% { clip: rect(69px, 9999px, 72px, 0px); }
}
@keyframes noise-anim { 
  0% { clip: rect(81px, 9999px, 74px, 0px); }
  5% { clip: rect(2px, 9999px, 29px, 0px); }
  10% { clip: rect(1px, 9999px, 15px, 0px); }
  15% { clip: rect(50px, 9999px, 8px, 0px); }
  20% { clip: rect(99px, 9999px, 79px, 0px); }
  25% { clip: rect(85px, 9999px, 15px, 0px); }
  30% { clip: rect(41px, 9999px, 53px, 0px); }
  35% { clip: rect(22px, 9999px, 36px, 0px); }
  40% { clip: rect(73px, 9999px, 79px, 0px); }
  45% { clip: rect(82px, 9999px, 100px, 0px); }
  50% { clip: rect(47px, 9999px, 96px, 0px); }
  55% { clip: rect(10px, 9999px, 44px, 0px); }
  60% { clip: rect(7px, 9999px, 24px, 0px); }
  65% { clip: rect(29px, 9999px, 88px, 0px); }
  70% { clip: rect(12px, 9999px, 44px, 0px); }
  75% { clip: rect(25px, 9999px, 57px, 0px); }
  80% { clip: rect(38px, 9999px, 35px, 0px); }
  85% { clip: rect(20px, 9999px, 96px, 0px); }
  90% { clip: rect(58px, 9999px, 44px, 0px); }
  95% { clip: rect(72px, 9999px, 41px, 0px); }
  100% { clip: rect(69px, 9999px, 72px, 0px); }
}
.error::after { content: attr(data-text); position: absolute; left: 2px; text-shadow: rgb(231, 74, 59) -1px 0px; top: 0px; color: rgb(90, 92, 105); background: rgb(248, 249, 252); overflow: hidden; clip: rect(0px, 900px, 0px, 0px); animation: 2s linear 0s infinite alternate-reverse none running noise-anim; }
@-webkit-keyframes noise-anim-2 { 
  0% { clip: rect(82px, 9999px, 93px, 0px); }
  5% { clip: rect(13px, 9999px, 71px, 0px); }
  10% { clip: rect(22px, 9999px, 90px, 0px); }
  15% { clip: rect(17px, 9999px, 11px, 0px); }
  20% { clip: rect(21px, 9999px, 91px, 0px); }
  25% { clip: rect(37px, 9999px, 33px, 0px); }
  30% { clip: rect(37px, 9999px, 80px, 0px); }
  35% { clip: rect(6px, 9999px, 49px, 0px); }
  40% { clip: rect(86px, 9999px, 60px, 0px); }
  45% { clip: rect(46px, 9999px, 83px, 0px); }
  50% { clip: rect(16px, 9999px, 83px, 0px); }
  55% { clip: rect(73px, 9999px, 36px, 0px); }
  60% { clip: rect(58px, 9999px, 98px, 0px); }
  65% { clip: rect(20px, 9999px, 93px, 0px); }
  70% { clip: rect(43px, 9999px, 67px, 0px); }
  75% { clip: rect(66px, 9999px, 75px, 0px); }
  80% { clip: rect(66px, 9999px, 41px, 0px); }
  85% { clip: rect(17px, 9999px, 47px, 0px); }
  90% { clip: rect(49px, 9999px, 68px, 0px); }
  95% { clip: rect(8px, 9999px, 85px, 0px); }
  100% { clip: rect(83px, 9999px, 50px, 0px); }
}
@keyframes noise-anim-2 { 
  0% { clip: rect(82px, 9999px, 93px, 0px); }
  5% { clip: rect(13px, 9999px, 71px, 0px); }
  10% { clip: rect(22px, 9999px, 90px, 0px); }
  15% { clip: rect(17px, 9999px, 11px, 0px); }
  20% { clip: rect(21px, 9999px, 91px, 0px); }
  25% { clip: rect(37px, 9999px, 33px, 0px); }
  30% { clip: rect(37px, 9999px, 80px, 0px); }
  35% { clip: rect(6px, 9999px, 49px, 0px); }
  40% { clip: rect(86px, 9999px, 60px, 0px); }
  45% { clip: rect(46px, 9999px, 83px, 0px); }
  50% { clip: rect(16px, 9999px, 83px, 0px); }
  55% { clip: rect(73px, 9999px, 36px, 0px); }
  60% { clip: rect(58px, 9999px, 98px, 0px); }
  65% { clip: rect(20px, 9999px, 93px, 0px); }
  70% { clip: rect(43px, 9999px, 67px, 0px); }
  75% { clip: rect(66px, 9999px, 75px, 0px); }
  80% { clip: rect(66px, 9999px, 41px, 0px); }
  85% { clip: rect(17px, 9999px, 47px, 0px); }
  90% { clip: rect(49px, 9999px, 68px, 0px); }
  95% { clip: rect(8px, 9999px, 85px, 0px); }
  100% { clip: rect(83px, 9999px, 50px, 0px); }
}
.error::before { content: attr(data-text); position: absolute; left: -2px; text-shadow: rgb(78, 115, 223) 1px 0px; top: 0px; color: rgb(90, 92, 105); background: rgb(248, 249, 252); overflow: hidden; clip: rect(0px, 900px, 0px, 0px); animation: 3s linear 0s infinite alternate-reverse none running noise-anim-2; }
footer.sticky-footer { padding: 2rem 0px; flex-shrink: 0; }
footer.sticky-footer .copyright { line-height: 1; font-size: 0.8rem; }
body.sidebar-toggled footer.sticky-footer { width: 100%; }
</style>

'''

html_additional = '''
<div class="card-header py-3">
  <h2 class="h4 m-0 font-weight-bold text-primary">Заявка#__order_id__</h2>
  <h2 class="h6 m-0 font-weight-bold text-primary">Статус запроса : <b>__moderator_status__</b> - <i class="text-secondary">__moderator_comment__</i></h2>
  <h2 class="h6 m-0 font-weight-bold text-primary">Статус утверждения : <b>__supervisor_status__</b> - <i class="text-secondary">__supervisor_comment__</i></h2>
  <br>
  <h2 class="h6 m-0 font-weight-bold text-secondary">Создано : <i class="text-secondary">__created_at__</i></h2>
  <h2 class="h6 m-0 font-weight-bold text-secondary">Изменено : <i class="text-secondary">__modified_at__</i></h2>
  
  
  
  
</div>
'''


html_end = '''
</body>
</html>
<style>
'''