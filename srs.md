B1 đọc và phân tích yêu cầu , hiểu về bussiness contest , xđ bussiness prolem, ngữ cảnh nghiệp vụ , KH cần giải quyết vấn đề mà hệ thống không xử lý được , mục tiêu , giá trị hệ thống , giá trị hệ thống mới khác gì hệ thống cũ
1. Tổng quan bài toán

Công ty ABC đang cung cấp dịch vụ đặt xe trực tuyến. Hiện tại khách hàng có thể yêu cầu xe thông qua tổng đài hoặc một ứng dụng đơn giản.
Tuy nhiên, hệ thống hiện tại chưa đáp ứng tốt quy trình vận hành khi số lượng khách hàng và tài xế tăng lên. Nhiều hoạt động vẫn phụ thuộc vào nhân viên và xử lý thủ công, trong khi khách hàng thiếu khả năng theo dõi chuyến đi theo thời gian thực.
Do đó, ABC muốn xây dựng một CAB System mới không chỉ phục vụ việc đặt xe mà còn quản lý xuyên suốt quy trình:
Đặt xe → Tìm tài xế → Phân công → Thực hiện chuyến → Tính cước → Thanh toán → Thông báo → Đánh giá → Báo cáo
Mục tiêu dài hạn là xây dựng một nền tảng có thể mở rộng thêm dịch vụ, phương thức thanh toán, kênh thông báo và các thành phần kỹ thuật mới mà không phải xây dựng lại toàn bộ hệ thống.

2. Business Context – Bối cảnh nghiệp vụ
2.1. Doanh nghiệp đang làm gì?
ABC cung cấp dịch vụ kết nối:
- Khách hàng có nhu cầu di chuyển.
- Tài xế cung cấp dịch vụ vận chuyển.
- Nhân viên vận hành quản lý và hỗ trợ toàn bộ hoạt động.
Hệ thống CAB đóng vai trò là nền tảng trung gian giúp ba nhóm này phối hợp với nhau.

2.2. Quy trình nghiệp vụ hiện tại
Quy trình hiện tại có thể mô tả khái quát:
- Khách hàng yêu cầu đặt xe.
- Yêu cầu được tiếp nhận qua tổng đài hoặc ứng dụng đơn giản.
- Nhân viên/tổ chức vận hành thực hiện việc tìm và phân công tài xế.
- Tài xế nhận chuyến.
- Tài xế thực hiện chuyến.
- Khách hàng thanh toán.
- Thông tin chuyến đi và thanh toán được lưu lại.
- Nhân viên vận hành hỗ trợ khi có sự cố.

Điểm yếu của quy trình là nhiều bước chưa được tự động hóa và dữ liệu chưa được quản lý tập trung.

3. Business Problem – Vấn đề nghiệp vụ

3.1. Vấn đề cốt lõi

ABC chưa có một nền tảng đặt xe đủ khả năng tự động hóa và quản lý xuyên suốt toàn bộ vòng đời của một chuyến xe.
Điều này dẫn đến các vấn đề:

Vấn đề 1 – Phân công tài xế thủ công
Việc tìm và phân công tài xế chủ yếu được thực hiện thủ công.

Hệ quả:

Mất thời gian xử lý.
Khó ưu tiên tài xế gần khách hàng.
Khó xử lý nhanh khi tài xế từ chối.
Khó mở rộng khi số lượng chuyến tăng.
Phụ thuộc nhiều vào nhân viên vận hành.

Vấn đề 2 – Khách hàng thiếu khả năng theo dõi chuyến
Khách hàng khó biết:
Hệ thống đang tìm tài xế hay chưa.
Tài xế nào đã nhận chuyến.
Tài xế đang ở đâu.
Khi nào tài xế dự kiến đến.
Chuyến đang ở trạng thái nào.
Điều này làm giảm tính minh bạch và trải nghiệm khách hàng.

Vấn đề 3 – Thanh toán chưa được quản lý tập trung
Thông tin thanh toán chưa được quản lý thống nhất.
Doanh nghiệp cần:
Tính cước.
Theo dõi kết quả thanh toán.
Hỗ trợ tiền mặt và thanh toán điện tử.
Xử lý giao dịch thất bại.
Tra cứu lịch sử giao dịch.

Vấn đề 4 – Khó mở rộng hệ thống
Hệ thống hiện tại không được định hướng như một nền tảng dài hạn.
Khi số lượng khách hàng, tài xế và chuyến đi tăng, hệ thống có nguy cơ khó đáp ứng tải.

Vấn đề 5 – Khó quản lý vận hành
Nhân viên cần theo dõi:
Chuyến đang diễn ra.
Trạng thái tài xế.
Khách hàng.
Phương tiện.
Giao dịch.
Các chuyến bị lỗi.

Nhưng hệ thống hiện tại chưa cung cấp một giao diện quản trị đầy đủ.

Vấn đề 6 – Thiếu dữ liệu phục vụ quản trị
Ban lãnh đạo cần các chỉ số:
Số lượng chuyến.
Doanh thu.
Tỷ lệ hoàn thành.
Tỷ lệ hủy.
Hiệu quả hoạt động tài xế.

Do đó hệ thống mới phải tạo ra dữ liệu có cấu trúc để phục vụ báo cáo.

Vấn đề 7 – Khó xử lý ngoại lệ
Các tình huống như:
Tài xế không phản hồi.
Tài xế từ chối.
Không tìm được tài xế.
Thanh toán thất bại.
Mất kết nối mạng.
Chuyến bị lỗi.
chưa được xác định đầy đủ về cách xử lý.

4. Business Need – Nhu cầu nghiệp vụ

ABC cần một nền tảng CAB có khả năng:

Tự động tiếp nhận yêu cầu đặt xe.
Tự động tìm tài xế phù hợp.
Theo dõi trạng thái chuyến.
Quản lý vị trí tài xế.
Tính cước.
Hỗ trợ nhiều phương thức thanh toán.
Gửi thông báo cho khách hàng và tài xế.
Quản lý khách hàng, tài xế, phương tiện và chuyến đi.
Phân quyền nhân viên vận hành.
Lưu vết các thao tác quan trọng.
Cung cấp báo cáo quản trị.

Có kiến trúc đủ linh hoạt để mở rộng trong tương lai.


B2 xđ stackholder , lập bảng cột 1 những stackholder nào , cột 2 vai trò của mỗi ng , dưới bảng vẽ ma trận stackholder metrix

