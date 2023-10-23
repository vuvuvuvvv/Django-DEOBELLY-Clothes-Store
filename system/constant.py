IMG_UNKNOWN_USER = "/static/images/users/unknown_user.png"
ADMIN_MAIL = "shinmovit256@gmail.com"
PHONE_CONTACT = "0123456789"
SENDER_MAIL = "shinmovit256@gmail.com"
COMPANY_ADDRESS = "130 ngõ 32 Đỗ Đức Dục, Mễ Trì, Nam Từ Liêm, Hà Nội"
SENDER_NAME = ("DE OBELLY-nonreply",)
STATUS_ACTIVE = 1
STATUS_INACTIVE = 0
STATUS_CHOICES = (
    (1, "Hoạt động"),
    (0, "Không hoạt động"),
)
ORDER_STATUS_CHOICE = (
    (0, 'Thất bại'),
    (1, 'Thành công'),
    (2, 'Đang xử lý'),
    (3, 'Đang vận chuyển')
)
ORDER_FAILED = 0
ORDER_SUCCESSFUL = 1
ORDER_PROCESSING = 2
ORDER_DELIVERING = 3
TRACKING_STATUS = {
    '0':'Thất bại',
    '1':'Thành công',
    '2':'Đang xử lý',
    '3':'Đang vận chuyển'
}
PRODUCT_PER_PAGE = 8