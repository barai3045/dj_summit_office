from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from management import views as mviews
from hr import views as hviews


router = routers.DefaultRouter()
router.register(r'approval', mviews.ApprovalViewSet)
router.register(r'quotation', mviews.QuotationViewSet)
router.register(r'quotation-item', mviews.QuotationItemViewSet)
router.register(r'titlequote', mviews.TitleQuoteViewSet)
router.register(r'titlequote-item', mviews.TitleQuoteItemViewSet)
router.register(r'purchaseorder', mviews.PurchaseOrderViewSet)
router.register(r'purchaseorder-term', mviews.PurchaseOrderTermViewSet)
router.register(r'paymentnote', mviews.PaymentNoteViewSet)
router.register(r'paymentnote-invoice', mviews.PaymentNoteInvoiceViewSet)
router.register(r'paymentnote-approval', mviews.PaymentNoteApprovalViewSet)
router.register(r'paymentothers', mviews.PaymentOthersViewSet)
router.register(r'paymentothers-item', mviews.PaymentOthersItemViewSet)

router.register(r'partitem', mviews.PartItemViewSet)
router.register(r'titleitem', mviews.TitleItemViewSet)
router.register(r'itemtype', mviews.ItemTypeViewSet)
router.register(r'measuringunit', mviews.MeasuringUnitViewSet)

router.register(r'vendor', mviews.VendorViewSet)
router.register(r'vendor-address', mviews.VendorAddressViewSet)
router.register(r'vendor-contact', mviews.VendorContactViewSet)
router.register(r'vendor-account', mviews.VendorAccountViewSet)


router.register(r'title', hviews.TitleViewSet)
router.register(r'office', hviews.OfficeViewSet)
router.register(r'employee', hviews.EmployeeViewSet)
router.register(r'employee-title', hviews.EmployeeTitleViewSet)
router.register(r'employee-office', hviews.EmployeeOfficeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include("home.urls", namespace='home')),
    path('payment/', include("management.payment.urls", namespace="payment")),
    path('order/', include("management.order.urls", namespace="order")),
    path('approval/', include("management.approval.urls", namespace="approval")),
    path('base/', include("management.base.urls", namespace="management_base")),
    path('', include("hr.employee.urls", namespace="employee")),
    path('api/', include("management.urls", namespace="management")),
    path('api/', include("hr.urls", namespace="hr")),
    path("__reload__/", include("django_browser_reload.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
