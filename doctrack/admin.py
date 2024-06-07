from doctrack.models import *


class AdminFormDTProject(admin.ModelAdmin):
    exclude = ('is_active', 'is_deleted', 'deleted_at', 'deleted_by')
    search_fields = ('name', 'description')
class AdminFormDTRegion(admin.ModelAdmin): exclude = ('is_active', 'is_deleted', 'deleted_at', 'deleted_by')
class AdminFormDTProjectRegion(admin.ModelAdmin): exclude = ('is_active', 'is_deleted', 'deleted_at', 'deleted_by')
class AdminFormDTWorkType(admin.ModelAdmin): exclude = ('is_active', 'is_deleted', 'deleted_at', 'deleted_by')
class AdminFormDTDocumentType(admin.ModelAdmin): exclude = ('is_active', 'is_deleted', 'deleted_at', 'deleted_by')
class AdminFormDTDocument(admin.ModelAdmin): exclude = ('is_active', 'is_deleted', 'deleted_at', 'deleted_by')
class AdminFormDTGroup(admin.ModelAdmin): exclude = ('is_active', 'is_deleted', 'deleted_at', 'deleted_by')
class AdminFormDTStatus(admin.ModelAdmin): exclude = ('is_active', 'is_deleted', 'deleted_at', 'deleted_by')
class AdminFormDTRequest(admin.ModelAdmin): exclude = ('is_active', 'is_deleted', 'deleted_at', 'deleted_by')
class AdminFormDTFileType(admin.ModelAdmin): exclude = ('is_active', 'is_deleted', 'deleted_at', 'deleted_by')
class DTCommentAdmin(admin.ModelAdmin): exclude = ('is_active', 'is_deleted', 'deleted_at', 'deleted_by')


admin.site.register(DTProject, AdminFormDTProject)
admin.site.register(DTRegion, AdminFormDTRegion)
admin.site.register(DTProjectRegion, AdminFormDTProjectRegion)
admin.site.register(DTWorkType, AdminFormDTWorkType)
admin.site.register(DTDocumentType, AdminFormDTDocumentType)
admin.site.register(DTDocument, AdminFormDTDocument)
admin.site.register(DTGroup, AdminFormDTGroup)
admin.site.register(DTStatus, AdminFormDTStatus)
admin.site.register(DTRequest, AdminFormDTRequest)
admin.site.register(DTFileType, AdminFormDTFileType)
admin.site.register(DTCounter)
admin.site.register(DTComment, DTCommentAdmin)