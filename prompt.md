# NHIỆM VỤ: KHẢO SÁT, NÂNG CẤP VÀ HOÀN THIỆN HỆ THỐNG ERP CHO DOANH NGHIỆP PHÂN PHỐI THỰC PHẨM BẢO VỆ SỨC KHỎE

## 1. Vai trò và mục tiêu

Bạn là Senior Software Engineer, Solution Architect và Business Analyst, có kinh nghiệm xây dựng hệ thống ERP, CRM, quản lý kho, bán hàng đa kênh, nhân sự và báo cáo tài chính quản trị.

Nhiệm vụ của bạn là khảo sát repository hiện tại, xác định kiến trúc và nghiệp vụ đang có, sau đó nâng cấp hệ thống thành ERP web online phục vụ hoạt động thực tế của doanh nghiệp.

**Nguyên tắc bắt buộc:**
- Không tự ý viết lại toàn bộ dự án.
- Không tự ý thay đổi framework, ngôn ngữ lập trình, cơ sở dữ liệu hoặc kiến trúc khi chưa chứng minh được sự cần thiết.
- Tái sử dụng tối đa code, component, API, database schema và chức năng hiện có nếu chúng phù hợp.
- Không xóa chức năng đang hoạt động chỉ vì muốn thiết kế lại.
- Không giả định chức năng đã hoàn thành khi mới chỉ tạo giao diện.
- Không tạo dữ liệu giả để làm cho báo cáo trông có vẻ hoạt động.
- Không phá vỡ dữ liệu hiện tại hoặc làm mất khả năng tương thích ngược mà không có phương án chuyển đổi.
- Ưu tiên hệ thống chạy được, nghiệp vụ chính xác, dễ bảo trì và có thể mở rộng.
- Nếu thiếu thông tin quan trọng, ghi rõ giả định, đưa ra phương án đề xuất và chỉ hỏi khi quyết định đó ảnh hưởng lớn đến dữ liệu, kiến trúc hoặc tính đúng đắn nghiệp vụ.

Mục tiêu cuối cùng là một hệ thống ERP có thể được nhân viên sử dụng hàng ngày, không phải chỉ là bản demo giao diện.

---

## 2. Bối cảnh doanh nghiệp

Doanh nghiệp kinh doanh và phân phối thực phẩm bảo vệ sức khỏe với ba nhãn hàng:

- PLUS
- CACAO
- TIBOKA

Doanh nghiệp có các kênh bán hàng:

1. TikTok Shop.
2. Shopee.
3. Bán sỉ cho tạp hóa, đại lý và điểm bán.
4. Bán trực tiếp cho khách hàng cuối.
5. Website riêng.

Mô hình nhân sự hiện tại gồm:

- Ban giám đốc/quản trị hệ thống.
- 01 nhân viên marketing.
- 01 nhân viên vận hành sàn TikTok Shop và Shopee.
- 02 nhân viên phát triển điểm bán, trực tiếp mang hàng từ công ty đi chào hàng, giao hàng cho đại lý và thu tiền.
- Nhân sự kho, kế toán hoặc chăm sóc khách hàng có thể được bổ sung trong tương lai.

Số lượng nhân viên có thể tăng. Hệ thống không được thiết kế cứng theo số lượng nhân viên hiện tại.

Hàng hóa được xuất từ kho công ty để bán qua các kênh khác nhau. Đối với nhân viên thị trường, hàng bàn giao được theo dõi tại kho riêng của từng nhân viên nhưng vẫn thuộc quyền sở hữu của công ty cho đến khi giao dịch bán hàng được xác nhận theo chính sách doanh nghiệp.

Doanh nghiệp cần quản lý tập trung sản phẩm, tồn kho, đơn hàng, khách hàng, đại lý, nhân viên, chấm công, KPI, chi phí, công nợ và lợi nhuận.

Ngôn ngữ giao diện mặc định: tiếng Việt.

Đơn vị tiền tệ: VNĐ.

Múi giờ: Asia/Ho_Chi_Minh.

Môi trường triển khai: web online, hỗ trợ đăng nhập từ nhiều thiết bị và nhiều địa điểm.

---

## 3. Giai đoạn 1 — Khảo sát codebase trước khi sửa

Trước khi thực hiện bất kỳ thay đổi lớn nào, hãy kiểm tra toàn bộ repository.

### 3.1. Khảo sát kỹ thuật

Xác định:

- Ngôn ngữ lập trình, framework frontend và backend.
- Cấu trúc thư mục và kiến trúc tổng thể.
- Cơ sở dữ liệu, ORM, migrations và các bảng hiện có.
- Cơ chế đăng nhập, xác thực, phân quyền.
- Các API và quy trình nghiệp vụ đã được triển khai.
- Những màn hình đã có, những màn hình còn thiếu.
- Cơ chế quản lý state, validation, xử lý lỗi và thông báo.
- Cách chạy local, cấu hình môi trường, build và deploy.
- Các thư viện tích hợp, file cấu hình, tác vụ nền và dịch vụ bên ngoài.
- Các test hiện có và tình trạng chạy test.
- Các lỗ hổng bảo mật hoặc nguy cơ mất dữ liệu dễ nhận thấy.

Đọc README, manifest, file cấu hình, schema database, migration, route, controller, service, model, middleware và test liên quan.

Không đọc hoặc xuất các bí mật từ `.env`, private key, access token hoặc thông tin đăng nhập. Chỉ xác định tên các biến môi trường cần thiết.

### 3.2. Lập bản đồ tính năng

Tạo tài liệu `docs/ERP_AUDIT.md` ghi rõ:

- Chức năng đã hoàn thành và hoạt động thực tế.
- Chức năng mới chỉ có giao diện.
- Chức năng đang lỗi hoặc chưa hoàn thiện.
- Chức năng chưa có.
- Bảng dữ liệu và quan hệ quan trọng.
- Các điểm cần cải tiến về bảo mật, hiệu năng và khả năng mở rộng.
- Các phần có thể tái sử dụng.
- Các rủi ro khi thay đổi hệ thống.

Không kết luận chức năng hoạt động chỉ dựa vào tên file hoặc việc có một trang giao diện.

### 3.3. Kế hoạch thực hiện

Tạo `docs/ERP_IMPLEMENTATION_PLAN.md` với:

- Kiến trúc hiện tại và kiến trúc mục tiêu.
- Danh sách module cần sửa, bổ sung hoặc giữ nguyên.
- Thứ tự triển khai và phụ thuộc giữa các module.
- Các thay đổi database dự kiến.
- Phương án migration và rollback.
- Kịch bản kiểm thử.
- Các quyết định cần xác nhận từ người dùng.

Sau khi hoàn tất khảo sát, có thể bắt đầu triển khai các hạng mục có yêu cầu rõ ràng và rủi ro thấp. Không cần dừng toàn bộ công việc chỉ vì những lựa chọn có thể cấu hình sau này.

Không thực hiện migration phá hủy, xóa dữ liệu, thay thế kiến trúc lớn hoặc triển khai production nếu chưa có phương án an toàn và sự chấp thuận cần thiết.

---

## 4. Giai đoạn 2 — Thiết kế mô hình dữ liệu nghiệp vụ

Thiết kế dựa trên database và ORM hiện có. Chỉ tạo hoặc thay đổi bảng khi cần thiết, bảo đảm khóa ngoại, ràng buộc dữ liệu và migration phù hợp.

Các nhóm thực thể nghiệp vụ cần được khảo sát và hỗ trợ khi cần:

### Danh mục và hàng hóa

- Brand.
- Product.
- SKU hoặc ProductVariant.
- UnitOfMeasure.
- Warehouse.
- WarehouseLocation nếu cần.
- InventoryLot.
- InventoryMovement.
- StockBalance hoặc cơ chế tính tồn phù hợp.
- StockTransfer.
- StockCount.
- StockAdjustment.
- StockReservation.

### Bán hàng và khách hàng

- Customer.
- CustomerAddress.
- CustomerGroup.
- SalesChannel.
- SalesOrder.
- SalesOrderItem.
- Shipment.
- Payment.
- PaymentAllocation.
- SalesReturn.
- ReturnItem.
- PriceList.
- Promotion nếu cần.
- SalesRepresentative hoặc quan hệ phân công nhân viên.

### Phân phối và nhân viên thị trường

- EmployeeWarehouse hoặc quan hệ kho được giao.
- StockHandover.
- StockReconciliation.
- CustomerAssignment.
- SalesVisit nếu cần.
- EmployeeCollection hoặc chứng từ thu tiền.
- WholesaleOrder.
- Receivable.
- ReceivableTransaction.

### Tài chính quản trị

- Expense.
- ExpenseCategory.
- CashTransaction.
- FinancialAccount.
- Payable nếu phát sinh nghiệp vụ.
- CostAllocation.
- ProfitReport hoặc dịch vụ tổng hợp báo cáo.

### Nhân sự

- Employee.
- Department.
- Role.
- Permission.
- AttendanceRecord.
- LeaveRequest.
- PayrollPeriod.
- PayrollRecord.
- Allowance.
- Bonus.
- KPIPlan.
- KPIResult.
- ApprovalRequest nếu cần.

### Kiểm soát và hệ thống

- User.
- AuditLog.
- Notification nếu cần.
- ImportJob hoặc ImportHistory.
- IntegrationConfig.
- IdempotencyKey hoặc cơ chế chống xử lý trùng khi tích hợp.

Không bắt buộc phải tạo tất cả các bảng trên nếu hệ thống hiện tại đã có mô hình tương đương. Ưu tiên thiết kế đúng nghiệp vụ hơn là tạo thật nhiều bảng.

---

## 5. Giai đoạn 3 — Module quản lý sản phẩm

Xây dựng hoặc hoàn thiện module quản lý sản phẩm với các trường:

- Mã sản phẩm, tên sản phẩm.
- Nhãn hàng: PLUS, CACAO, TIBOKA.
- SKU/mã hàng duy nhất.
- Danh mục sản phẩm.
- Quy cách đóng gói.
- Đơn vị tính và quy đổi đơn vị nếu cần.
- Mã vạch nếu có.
- Giá vốn.
- Giá bán lẻ.
- Giá bán sỉ.
- Giá bán theo bảng giá hoặc nhóm khách hàng.
- Trạng thái hoạt động.
- Mô tả và hình ảnh.
- Thông tin lô và hạn sử dụng.
- Ngưỡng cảnh báo tồn kho.
- Ngưỡng cảnh báo hàng sắp hết hạn.

Cho phép quản trị viên thay đổi giá và quản lý lịch sử thay đổi giá khi cần.

Không ghi đè giá của các đơn hàng lịch sử khi bảng giá thay đổi. Mỗi đơn hàng phải lưu lại giá và các khoản chiết khấu đã áp dụng tại thời điểm giao dịch.

Hỗ trợ tìm kiếm, lọc theo nhãn hàng, SKU, danh mục, trạng thái và xuất dữ liệu.

---

## 6. Giai đoạn 4 — Module kho và lô hàng

Đây là module có mức độ ưu tiên cao.

### 6.1. Quản lý kho

Hỗ trợ tối thiểu:

- Kho tổng của công ty.
- Kho hàng được bàn giao cho từng nhân viên thị trường.
- Các kho hoặc địa điểm khác có thể bổ sung trong tương lai.

Tồn kho phải theo dõi theo SKU, kho và lô hàng.

### 6.2. Nghiệp vụ kho

- Nhập hàng.
- Xuất hàng bán.
- Bàn giao hàng cho nhân viên.
- Điều chuyển hàng giữa các kho.
- Nhân viên trả hàng về kho công ty.
- Kiểm kê.
- Điều chỉnh tồn có lý do và người phê duyệt.
- Ghi nhận hàng hỏng, hàng hết hạn và hàng cách ly.
- Ghi nhận hàng khách trả về.
- Theo dõi lịch sử nhập xuất tồn.

Mọi giao dịch kho phải lưu thời gian, người thực hiện, kho nguồn, kho đích nếu có, SKU, lô, số lượng, loại nghiệp vụ và chứng từ liên quan.

Không cho phép tồn kho âm nếu chưa có chính sách được phê duyệt rõ ràng. Nếu nghiệp vụ cho phép ngoại lệ, phải có quyền đặc biệt và audit log.

### 6.3. Lô hàng và hạn sử dụng

Mỗi lô cần quản lý:

- Mã lô.
- SKU.
- Ngày sản xuất nếu có.
- Hạn sử dụng.
- Ngày nhập.
- Số lượng nhập.
- Số lượng tồn.
- Giá vốn.
- Trạng thái chất lượng.

Ưu tiên xuất theo FEFO: First Expired, First Out.

Cảnh báo các lô sắp hết hạn theo các mốc ngày có thể cấu hình.

Không tự động bán hoặc xuất hàng đã hết hạn. Hàng lỗi, hết hạn hoặc bị cách ly không được tính vào lượng hàng có thể bán.

### 6.4. Tính tồn

Tồn hiện tại phải có thể đối chiếu với sổ giao dịch kho.

Nếu dùng bảng số dư để tăng hiệu năng, cần bảo đảm cập nhật nguyên tử và có cách đối chiếu với các giao dịch gốc.

Không cho phép hai yêu cầu đồng thời xuất vượt số lượng tồn do race condition.

---

## 7. Giai đoạn 5 — Module bán hàng đa kênh

Mỗi đơn hàng phải xác định rõ:

- Mã đơn hàng nội bộ.
- Kênh bán hàng.
- Nguồn đơn.
- Khách hàng.
- Nhân viên phụ trách.
- Kho xuất hàng.
- Sản phẩm và SKU.
- Số lượng.
- Đơn giá.
- Chiết khấu.
- Phí vận chuyển do từng bên chịu.
- Tổng tiền.
- Số tiền đã thu.
- Số tiền còn phải thu.
- Trạng thái đơn.
- Trạng thái giao hàng.
- Trạng thái thanh toán.
- Thời điểm tạo, xác nhận, giao hàng, hoàn tất và hủy.
- Thông tin lô xuất thực tế khi xuất kho.

### 7.1. Bán sỉ đại lý

Hỗ trợ:

- Tạo khách hàng đại lý.
- Gán nhân viên phụ trách.
- Quản lý địa chỉ và thông tin liên hệ.
- Tạo đơn hàng.
- Áp dụng giá sỉ và chiết khấu.
- Giao hàng từ kho công ty hoặc kho nhân viên.
- Thu tiền ngay hoặc ghi nhận công nợ.
- Thu một phần hoặc nhiều lần.
- Theo dõi lịch sử giao dịch.
- Theo dõi công nợ theo từng đại lý.
- Trả hàng, đổi hàng và điều chỉnh công nợ.

Không cho phép người dùng tự ý xóa giao dịch công nợ đã ghi nhận. Việc sửa sai cần dùng nghiệp vụ điều chỉnh có kiểm soát.

### 7.2. Bán trực tiếp

Hỗ trợ tạo đơn nhanh, chọn sản phẩm, tính tổng tiền, ghi nhận thanh toán, xuất hàng và lưu lịch sử mua hàng.

Nếu khách chưa có tài khoản, cho phép tạo khách hàng mới với thông tin tối thiểu phù hợp.

### 7.3. TikTok Shop và Shopee

Giai đoạn đầu:

- Nhập đơn thủ công.
- Import Excel/CSV.
- Kiểm tra dữ liệu trước khi nhập.
- Hiển thị lỗi theo từng dòng.
- Chống nhập trùng đơn.
- Ánh xạ mã sản phẩm trên sàn với SKU nội bộ.
- Ghi nhận doanh thu theo đơn, giảm giá, phí sàn, vận chuyển, hoàn hàng và khoản quyết toán nếu có dữ liệu.
- Theo dõi trạng thái đơn và trạng thái đối soát.
- Hỗ trợ lọc theo sàn và kỳ báo cáo.

Thiết kế lớp adapter/service để có thể tích hợp API chính thức của TikTok Shop và Shopee trong tương lai mà không phải viết lại toàn bộ nghiệp vụ đơn hàng.

Không giả lập rằng đã kết nối API khi chưa có thông tin xác thực và chưa thực hiện kiểm thử tích hợp thực tế.

Không đồng nhất tổng giá trị đơn hàng với số tiền thực nhận từ sàn.

### 7.4. Website

Cho phép tiếp nhận đơn từ website hoặc nhập đơn từ nguồn website.

Thiết kế API và cơ chế liên kết đơn hàng phù hợp để tích hợp website trong tương lai. Chỉ triển khai storefront hoặc checkout nếu hệ thống hiện tại có phạm vi đó hoặc được xác định rõ trong kế hoạch.

### 7.5. Trạng thái đơn hàng

Thiết kế trạng thái rõ ràng, tránh gộp mọi nghiệp vụ vào một trường trạng thái duy nhất.

Cần phân biệt tối thiểu:

- Trạng thái xử lý đơn.
- Trạng thái giao hàng.
- Trạng thái thanh toán.
- Trạng thái đối soát.
- Trạng thái đổi trả.

Quy định các chuyển trạng thái hợp lệ và hành động tương ứng.

Không tự động ghi nhận doanh thu, xuất kho hoặc thanh toán nhiều lần khi đơn hàng được cập nhật trạng thái lặp lại.

---

## 8. Giai đoạn 6 — Quản lý kho nhân viên thị trường

Đây là nghiệp vụ đặc thù cần thiết kế chính xác.

Mỗi nhân viên thị trường có thể được gán một kho riêng.

### 8.1. Bàn giao hàng

Khi công ty giao hàng cho nhân viên:

- Tạo phiếu bàn giao.
- Chọn nhân viên, kho nguồn, kho đích.
- Ghi nhận SKU, lô và số lượng.
- Ghi nhận thời gian, người giao, người nhận.
- Cập nhật tồn kho bằng giao dịch điều chuyển.
- Không ghi nhận doanh thu.
- Không tự động ghi nhận nhân viên mua hàng.
- Hàng vẫn thuộc sở hữu công ty.

### 8.2. Bán hàng từ kho nhân viên

Khi nhân viên bán cho đại lý:

- Tạo đơn hàng gắn với nhân viên phụ trách.
- Xuất hàng từ kho nhân viên theo lô thực tế.
- Ghi nhận doanh thu theo chính sách ghi nhận doanh thu.
- Ghi nhận khoản khách đã thanh toán và khoản còn nợ.
- Nếu nhân viên thu tiền hộ, ghi nhận khoản tiền đang do nhân viên giữ và chưa nộp về công ty.

### 8.3. Đối soát kho nhân viên

Cung cấp báo cáo:

- Tồn đầu kỳ.
- Hàng nhận từ công ty.
- Hàng nhận điều chuyển.
- Hàng đã bán.
- Hàng trả về.
- Hàng hỏng hoặc hết hạn.
- Điều chỉnh được phê duyệt.
- Tồn cuối kỳ theo hệ thống.
- Tồn thực tế kiểm kê.
- Chênh lệch.
- Số tiền đã thu.
- Số tiền đã nộp công ty.
- Tiền còn phải nộp.
- Công nợ khách hàng phụ trách.

Công thức số lượng phải được xác định rõ:

Tồn cuối kỳ = Tồn đầu kỳ + Nhập và điều chuyển đến - Xuất bán - Điều chuyển đi - Các xuất giảm tồn hợp lệ ± Điều chỉnh được phê duyệt.

Không tính cùng một khoản tiền vừa là doanh thu mới vừa là khoản thu công nợ cũ.

### 8.4. Thu tiền hộ

Tách riêng:

- Doanh thu của đơn hàng.
- Khoản phải thu của khách hàng.
- Tiền nhân viên đã thu.
- Tiền nhân viên đã nộp.
- Số tiền còn phải nộp.
- Chênh lệch cần đối soát.

Không tự động ghi nhận tiền đã về quỹ công ty chỉ vì nhân viên xác nhận đã thu.

---

## 9. Giai đoạn 7 — CRM và quản lý điểm bán

Xây dựng hồ sơ khách hàng tập trung gồm:

- Mã khách hàng.
- Tên cá nhân hoặc doanh nghiệp.
- Nhóm khách hàng.
- Kênh khách hàng.
- Số điện thoại, email và địa chỉ nếu có.
- Thông tin cửa hàng/đại lý.
- Nhân viên phụ trách.
- Lịch sử mua hàng.
- Tổng doanh số.
- Công nợ.
- Lịch sử thanh toán.
- Lịch sử đổi trả.
- Ghi chú chăm sóc.
- Trạng thái khách hàng.

Hỗ trợ phân loại đại lý, tạp hóa, khách lẻ, khách website và khách mua qua sàn khi dữ liệu cho phép.

Nhân viên thị trường có thể ghi nhận điểm bán tiềm năng, kết quả chào hàng và lịch sử tiếp xúc.

Hỗ trợ:

- Tạo điểm bán mới.
- Giao khách hàng cho nhân viên.
- Chuyển giao khách hàng có lưu lịch sử.
- Tìm kiếm khách hàng trùng lặp.
- Lọc khách hàng theo nhân viên, khu vực, doanh số và công nợ.
- Theo dõi khách hàng chưa mua lại nếu có đủ dữ liệu.
- Xuất danh sách theo quyền được cấp.

Không cho nhân viên xem toàn bộ thông tin khách hàng của doanh nghiệp nếu họ không được phân quyền.

---

## 10. Giai đoạn 8 — Đổi trả, hàng lỗi và hàng hết hạn

Hỗ trợ tạo chứng từ đổi trả liên kết với đơn hàng gốc khi có thể.

Phải ghi rõ:

- Lý do đổi trả.
- Sản phẩm và số lượng.
- Lô hàng.
- Tình trạng hàng trả về.
- Người tiếp nhận.
- Phương án xử lý.
- Số tiền hoàn hoặc điều chỉnh công nợ.
- Ảnh hoặc tài liệu minh chứng nếu cần.
- Người phê duyệt.

Phân biệt:

1. Hàng trả về còn đủ điều kiện bán: nhập vào kho khả dụng sau khi được xác nhận.
2. Hàng cần kiểm tra: đưa vào kho cách ly.
3. Hàng hỏng hoặc không đủ điều kiện bán: ghi nhận riêng và xử lý theo quy trình.
4. Hàng hết hạn: không nhập lại vào tồn kho có thể bán.
5. Hàng hoàn từ sàn: chỉ ghi nhận tăng tồn khả dụng khi thực tế nhận hàng và xác nhận tình trạng.

Đơn hoàn tiền, đơn hoàn hàng và giao dịch điều chỉnh kho phải được liên kết để không hoàn tiền hoặc nhập hàng hai lần.

---

## 11. Giai đoạn 9 — Chi phí và báo cáo lãi lỗ quản trị

Xây dựng module ghi nhận chi phí:

- Quảng cáo và marketing.
- Lương nhân viên.
- Phụ cấp.
- Thưởng.
- Vận chuyển.
- Đóng gói.
- Phí sàn và phí thanh toán.
- Thuê văn phòng.
- Thuê kho.
- Chi phí vận hành khác.

Mỗi khoản chi cần có:

- Mã chứng từ.
- Danh mục.
- Số tiền.
- Ngày phát sinh.
- Ngày thanh toán.
- Người tạo.
- Người phê duyệt nếu cần.
- Trạng thái thanh toán.
- Phương thức thanh toán.
- Tài khoản/quỹ liên quan.
- Kênh bán hoặc bộ phận chịu chi phí nếu có.
- Nhãn hàng liên quan nếu xác định được.
- File minh chứng nếu cần.

Phân biệt chi phí đã phát sinh với tiền đã thanh toán.

### 11.1. Báo cáo bán hàng

Hỗ trợ lọc theo:

- Ngày, tuần, tháng, quý, năm.
- Nhãn hàng.
- SKU.
- Kênh bán.
- Nhân viên.
- Đại lý.
- Trạng thái đơn hàng.

Hiển thị tối thiểu:

- Số đơn.
- Số lượng bán.
- Tổng giá trị đơn hàng.
- Giảm giá.
- Doanh thu thuần theo quy ước được xác định.
- Giá vốn hàng đã bán.
- Lợi nhuận gộp.
- Phí sàn.
- Chi phí vận chuyển do doanh nghiệp chịu.
- Các chi phí trực tiếp khác.
- Lợi nhuận đóng góp theo kênh nếu đủ dữ liệu.

### 11.2. Báo cáo lợi nhuận

Thiết kế báo cáo theo nhiều tầng:

1. Tổng giá trị bán hàng.
2. Trừ giảm giá, hủy đơn và khoản điều chỉnh liên quan để xác định doanh thu thuần phù hợp.
3. Trừ giá vốn hàng bán để tính lợi nhuận gộp.
4. Trừ các chi phí trực tiếp liên quan để tính lợi nhuận đóng góp.
5. Trừ chi phí nhân sự và chi phí vận hành được phân bổ để ước tính lợi nhuận quản trị.

Hiển thị rõ công thức và khoản mục được đưa vào từng tầng.

Không gọi lợi nhuận gộp là lợi nhuận ròng.

Không tự ý cộng toàn bộ chi phí quảng cáo, lương và phí sàn vào từng đơn hàng nếu chưa có quy tắc phân bổ rõ ràng.

Cho phép phân bổ chi phí theo các tiêu chí có thể cấu hình, chẳng hạn:

- Kênh bán.
- Nhãn hàng.
- Bộ phận.
- Thời gian.
- Doanh thu hoặc tiêu chí quản trị khác.

Báo cáo phải hiển thị các khoản chưa phân bổ riêng biệt khi chưa đủ dữ liệu.

### 11.3. Dòng tiền và đối soát

Phân biệt:

- Doanh thu đã ghi nhận.
- Tiền khách đã thanh toán.
- Tiền đã về tài khoản công ty.
- Tiền nhân viên đang giữ.
- Công nợ phải thu.
- Chi phí đã phát sinh.
- Tiền đã chi.
- Khoản quyết toán với sàn.
- Tiền thực nhận sau phí và các khoản điều chỉnh.

Không lấy số tiền thực nhận từ ngân hàng hoặc sàn làm doanh thu duy nhất, vì thời điểm ghi nhận doanh thu và thanh toán có thể khác nhau.

### 11.4. Giới hạn báo cáo

Đây là hệ thống báo cáo quản trị nội bộ. Không tự nhận hệ thống đã đáp ứng đầy đủ chế độ kế toán, hóa đơn điện tử, thuế hoặc báo cáo pháp định nếu chưa triển khai và kiểm định các nghiệp vụ đó.

---

## 12. Giai đoạn 10 — Quản lý nhân sự, chấm công và KPI

### 12.1. Hồ sơ nhân sự

Quản lý:

- Mã nhân viên.
- Họ tên.
- Bộ phận.
- Chức vụ.
- Ngày bắt đầu làm việc.
- Trạng thái làm việc.
- Thông tin liên hệ cần thiết.
- Mức lương cơ bản.
- Phụ cấp.
- Quy tắc thưởng.
- Người quản lý trực tiếp.

Chỉ người được cấp quyền mới được xem thông tin lương và thông tin cá nhân nhạy cảm.

### 12.2. Chấm công và nghỉ phép

Hỗ trợ:

- Check-in/check-out.
- Ngày công và giờ công.
- Đi muộn/về sớm.
- Nghỉ phép.
- Yêu cầu nghỉ phép và phê duyệt.
- Điều chỉnh công có lý do.
- Lịch sử thay đổi.
- Tổng hợp công theo tháng.

Nếu chưa có tích hợp máy chấm công hoặc GPS, không giả lập dữ liệu vị trí. Có thể triển khai chấm công cơ bản trước và thiết kế điểm mở rộng sau.

### 12.3. Lương, phụ cấp và thưởng

Hỗ trợ cấu hình:

- Lương cơ bản.
- Phụ cấp.
- Thưởng KPI.
- Hoa hồng hoặc thưởng doanh số.
- Khoản khấu trừ được phép.
- Điều chỉnh có phê duyệt.
- Kỳ lương.
- Bảng lương dự kiến.
- Chốt lương.
- Lịch sử thay đổi.

Không tự ý tạo công thức tính lương theo luật hoặc chính sách chưa được xác nhận.

### 12.4. KPI theo vai trò

KPI phải cấu hình được theo nhân viên, vai trò và kỳ đánh giá.

Ví dụ:

**Nhân viên phát triển điểm bán**
- Số điểm bán mới.
- Số điểm bán phát sinh đơn.
- Doanh thu.
- Số lượng bán.
- Lợi nhuận đóng góp.
- Tỷ lệ thu hồi công nợ.
- Tỷ lệ đối soát hàng chính xác.
- Tỷ lệ khách hàng mua lại.

**Nhân viên vận hành sàn**
- Doanh thu theo sàn.
- Số đơn hoàn tất.
- Giá trị đơn hàng trung bình.
- Tỷ lệ hủy và hoàn.
- Phí sàn.
- Lợi nhuận đóng góp theo kênh.
- Mức độ chính xác của đối soát.

**Nhân viên marketing**
- Ngân sách sử dụng.
- Số nội dung đã hoàn thành.
- Chỉ số tiếp cận hoặc tương tác.
- Số khách hàng tiềm năng.
- Hiệu quả chiến dịch khi có dữ liệu đo lường.

Không đánh giá nhân viên chỉ dựa vào doanh thu nếu mục tiêu quản trị còn bao gồm lợi nhuận, chất lượng khách hàng và thu hồi công nợ.

Phân biệt chỉ số mục tiêu, kết quả thực tế và tỷ lệ hoàn thành.

---

## 13. Giai đoạn 11 — Phân quyền và bảo mật

Triển khai RBAC kết hợp phạm vi dữ liệu.

Các vai trò mặc định cần hỗ trợ:

- Super Admin.
- Giám đốc/quản trị doanh nghiệp.
- Quản lý kinh doanh.
- Quản lý kho.
- Nhân viên kho.
- Nhân viên phát triển điểm bán.
- Nhân viên vận hành sàn.
- Nhân viên marketing.
- Nhân sự.
- Tài chính quản trị.
- Chăm sóc khách hàng.

Có thể gộp hoặc bổ sung vai trò tùy tình trạng nhân sự thực tế.

### 13.1. Phạm vi dữ liệu

Ví dụ:

- Nhân viên thị trường chỉ xem kho, khách hàng, đơn hàng và KPI thuộc phạm vi được giao.
- Nhân viên marketing không mặc định được xem bảng lương.
- Nhân viên vận hành sàn được xem và xử lý đơn thuộc kênh được phân công.
- Nhân viên kho được thao tác các nghiệp vụ kho nhưng không tự duyệt điều chỉnh do mình tạo nếu chính sách yêu cầu kiểm soát chéo.
- Quản lý được xem dữ liệu trong phạm vi bộ phận.
- Ban giám đốc được xem dashboard tổng hợp.
- Chỉ người có quyền mới được thay đổi giá, xóa mềm dữ liệu, duyệt chi phí, chốt lương hoặc điều chỉnh công nợ.

Không chỉ ẩn nút trên frontend. Phải kiểm tra quyền ở backend/API cho mọi thao tác nhạy cảm.

### 13.2. Audit log

Ghi nhận tối thiểu:

- Người thực hiện.
- Thời gian.
- Hành động.
- Đối tượng bị tác động.
- Giá trị trước và sau đối với thay đổi quan trọng.
- Lý do điều chỉnh khi cần.
- Kết quả thao tác.

Audit log phải được bảo vệ khỏi chỉnh sửa trái phép.

### 13.3. An toàn ứng dụng

- Xác thực và phân quyền an toàn.
- Validate dữ liệu phía backend.
- Bảo vệ khỏi SQL injection, XSS, CSRF và các lỗi phù hợp với kiến trúc.
- Quản lý session/token an toàn.
- Giới hạn truy cập endpoint nhạy cảm.
- Không để lộ secrets.
- Không trả dữ liệu vượt quyền trong API.
- Có sao lưu và phương án khôi phục.
- Không xóa cứng chứng từ tài chính hoặc kho đã phát sinh nếu cần giữ dấu vết kiểm toán.

---

## 14. Giai đoạn 12 — Dashboard và báo cáo thống kê

Xây dựng dashboard theo quyền và vai trò.

### Dashboard giám đốc

- Tổng doanh thu thuần.
- Lợi nhuận gộp.
- Lợi nhuận đóng góp.
- Chi phí theo kỳ.
- Doanh số theo nhãn hàng.
- Doanh số theo kênh.
- Doanh số theo nhân viên.
- Công nợ phải thu.
- Tiền đã thu và tiền còn phải nộp.
- Tồn kho và giá trị tồn.
- Hàng sắp hết hạn.
- Hàng hỏng, hàng hết hạn.
- KPI nhân sự.
- Các cảnh báo cần xử lý.

### Dashboard kho

- Tồn theo SKU và lô.
- Nhập/xuất trong kỳ.
- Lô sắp hết hạn.
- Hàng cách ly.
- Hàng tồn thấp.
- Hàng đang nằm tại kho nhân viên.
- Chênh lệch kiểm kê.

### Dashboard kinh doanh

- Đơn hàng theo trạng thái.
- Doanh thu theo kênh.
- Điểm bán mới.
- Khách hàng phát sinh đơn.
- Công nợ đến hạn.
- Hiệu quả từng nhân viên.

### Dashboard nhân viên

Chỉ hiển thị dữ liệu của bản thân hoặc phạm vi được phân quyền.

Tất cả biểu đồ phải lấy dữ liệu thực từ backend. Có bộ lọc thời gian, nhãn hàng, kênh bán và nhân viên khi phù hợp.

Cần hỗ trợ xuất báo cáo CSV/Excel nếu thư viện hiện tại cho phép triển khai an toàn.

---

## 15. Giai đoạn 13 — Giao diện và trải nghiệm sử dụng

Ưu tiên giao diện quản trị rõ ràng, nhất quán và thuận tiện khi dùng hàng ngày.

Yêu cầu:

- Sidebar điều hướng theo module.
- Dashboard phù hợp với từng vai trò.
- Bảng dữ liệu có tìm kiếm, lọc, sắp xếp và phân trang.
- Form tạo/sửa có validation và thông báo lỗi rõ ràng.
- Trạng thái loading, empty state và error state.
- Hộp xác nhận trước các thao tác quan trọng.
- Giao diện responsive trên máy tính, máy tính bảng và điện thoại.
- Định dạng tiền tệ VNĐ thống nhất.
- Hiển thị ngày giờ theo múi giờ Việt Nam.
- Không dùng dữ liệu hard-code thay cho dữ liệu backend.
- Không để nút thao tác không có chức năng thực tế.
- Không tạo các màn hình chỉ mang tính trang trí.

Tái sử dụng design system, component và thư viện hiện tại nếu hợp lý. Không cài thêm thư viện lớn nếu không cần thiết.

---

## 16. Giai đoạn 14 — Kiến trúc tích hợp trong tương lai

Chuẩn bị các điểm mở rộng:

- API chính thức của TikTok Shop.
- API chính thức của Shopee.
- Website bán hàng.
- Dịch vụ vận chuyển.
- Email hoặc thông báo nội bộ.
- Phần mềm kế toán.
- Thiết bị chấm công.

Không triển khai tích hợp giả lập dưới danh nghĩa tích hợp thực tế.

Đối với mọi tích hợp bên ngoài:

- Tách cấu hình và thông tin xác thực khỏi code.
- Có log và trạng thái đồng bộ.
- Có cơ chế retry phù hợp.
- Chống xử lý trùng.
- Có cách xử lý lỗi từng phần.
- Có khả năng đối soát dữ liệu.
- Không làm hỏng dữ liệu nội bộ nếu dịch vụ bên ngoài ngừng hoạt động.

---

## 17. Giai đoạn 15 — Nguyên tắc kỹ thuật và tính toàn vẹn dữ liệu

Các nghiệp vụ có tác động đồng thời đến nhiều bảng phải dùng transaction phù hợp.

Ví dụ:

- Xác nhận đơn và xuất kho.
- Điều chuyển kho.
- Ghi nhận thanh toán và phân bổ công nợ.
- Xử lý hàng trả về.
- Chốt lương.
- Duyệt điều chỉnh tồn.

Cần bảo đảm:

- Tiền được lưu bằng kiểu dữ liệu chính xác, không dùng floating point tùy tiện để tính toán tài chính.
- Số lượng có độ chính xác phù hợp với đơn vị hàng hóa.
- Các giao dịch có ID và quan hệ chứng từ rõ ràng.
- Chống tạo trùng đơn hoặc thanh toán khi retry.
- Không tự động tạo bút toán hoặc giao dịch lặp khi người dùng bấm nhiều lần.
- Không sửa lịch sử bằng cách ghi đè các giao dịch đã xác nhận; sử dụng giao dịch đảo hoặc điều chỉnh khi phù hợp.
- Báo cáo có thể đối chiếu về các dữ liệu gốc.
- Trạng thái nghiệp vụ phải được định nghĩa rõ ràng.
- Tách thời điểm tạo giao dịch, thời điểm phát sinh nghiệp vụ và thời điểm thanh toán nếu cần.

Khi thêm trường hoặc bảng, phải tạo migration có khả năng triển khai an toàn và có phương án rollback phù hợp. Không xóa hoặc đổi nghĩa dữ liệu hiện có một cách âm thầm.

---

## 18. Giai đoạn 16 — Kiểm thử bắt buộc

Trước khi kết luận hoàn thành, phải thực hiện các kiểm thử phù hợp với dự án.

### 18.1. Kiểm thử sản phẩm và kho

1. Tạo sản phẩm và SKU thuộc PLUS, CACAO, TIBOKA.
2. Nhập nhiều lô có hạn sử dụng khác nhau.
3. Kiểm tra tồn theo lô.
4. Bàn giao hàng từ kho công ty sang kho nhân viên.
5. Xác nhận việc bàn giao không tạo doanh thu.
6. Bán hàng từ kho nhân viên và kiểm tra giảm tồn.
7. Trả hàng về kho.
8. Kiểm tra hàng hỏng, hàng hết hạn và hàng cách ly.
9. Kiểm kê và đối chiếu số liệu.
10. Kiểm tra hai giao dịch đồng thời không làm tồn âm ngoài chính sách.

### 18.2. Kiểm thử bán hàng và công nợ

1. Tạo đơn sỉ thanh toán ngay.
2. Tạo đơn sỉ có công nợ.
3. Thu nhiều lần cho một khoản phải thu.
4. Bán trực tiếp.
5. Import đơn hàng từ file.
6. Import lại cùng file để kiểm tra chống trùng.
7. Xử lý đơn hủy và đơn hoàn.
8. Kiểm tra không ghi nhận trùng doanh thu hoặc xuất kho.
9. Đối soát đơn hàng sàn với khoản quyết toán.

### 18.3. Kiểm thử tài chính

1. Đối chiếu doanh thu, giảm giá và giá vốn.
2. Đối chiếu phí sàn và phí vận chuyển.
3. Đối chiếu chi phí quảng cáo, lương và tiền thuê.
4. Kiểm tra báo cáo theo nhãn hàng và kênh.
5. Kiểm tra tiền thu khác với doanh thu ghi nhận.
6. Kiểm tra công nợ không bị tính trùng.
7. Kiểm tra chi phí chưa thanh toán và chi phí đã thanh toán.
8. Kiểm tra kết quả báo cáo bằng bộ dữ liệu mẫu có đáp án tính toán độc lập.

### 18.4. Kiểm thử nhân sự và phân quyền

1. Check-in/check-out.
2. Tạo và duyệt nghỉ phép.
3. Tính tổng công.
4. Tạo bảng lương và thưởng.
5. Tính KPI theo kỳ.
6. Nhân viên không thể xem dữ liệu ngoài phạm vi.
7. Nhân viên không thể tự cấp quyền.
8. Người không có quyền không thể duyệt điều chỉnh kho, chi phí hoặc lương.
9. Kiểm tra audit log.
10. Kiểm tra bảo vệ API, không chỉ giao diện.

### 18.5. Kiểm thử hồi quy

- Chạy test hiện có.
- Chạy lint/typecheck/build nếu dự án hỗ trợ.
- Chạy migration trên môi trường thử nghiệm.
- Kiểm tra các luồng cũ vẫn hoạt động.
- Kiểm tra xử lý lỗi và các trạng thái không có dữ liệu.
- Kiểm tra giao diện trên kích thước màn hình phổ biến.

Nếu không thể chạy test vì thiếu môi trường, phải ghi rõ lý do và những gì chưa được xác minh. Không tuyên bố test đã pass khi chưa thực sự chạy.

---

## 19. Giai đoạn 17 — Thứ tự triển khai

Triển khai theo từng module, tránh sửa toàn bộ hệ thống cùng lúc.

### Phase 0: Khảo sát

- Đọc codebase.
- Lập bản đồ chức năng.
- Xác định rủi ro.
- Đề xuất kế hoạch.

### Phase 1: Nền tảng

- Đăng nhập.
- Phân quyền.
- Nhân sự cơ bản.
- Danh mục nhãn hàng, sản phẩm và SKU.
- Audit log.
- Migration và dữ liệu nền.

### Phase 2: Kho

- Kho tổng.
- Lô và hạn sử dụng.
- Nhập xuất tồn.
- Bàn giao và điều chuyển.
- Kho nhân viên.
- Kiểm kê.

### Phase 3: Bán hàng và CRM

- Khách hàng và đại lý.
- Đơn hàng đa kênh.
- Bán sỉ và công nợ.
- Bán trực tiếp.
- Import đơn sàn.
- Đổi trả.

### Phase 4: Tài chính quản trị

- Thu tiền và nộp tiền.
- Chi phí.
- Đối soát.
- Giá vốn.
- Báo cáo doanh thu, lợi nhuận và dòng tiền.

### Phase 5: Nhân sự

- Chấm công.
- Nghỉ phép.
- Lương, phụ cấp, thưởng.
- KPI.
- Phê duyệt.

### Phase 6: Dashboard và hoàn thiện

- Dashboard giám đốc.
- Dashboard theo vai trò.
- Xuất báo cáo.
- Tối ưu giao diện.
- Tối ưu hiệu năng.
- Kiểm thử toàn hệ thống.

Thứ tự trên là định hướng. Có thể điều chỉnh nếu kiến trúc hiện tại đã có module hoàn chỉnh hoặc có phụ thuộc kỹ thuật khác, nhưng phải giải thích lý do.

Sau mỗi phase, chạy kiểm thử liên quan và báo cáo những gì đã hoàn thành trước khi tiếp tục các thay đổi rủi ro cao.

---

## 20. Giai đoạn 18 — Tiêu chí nghiệm thu

Một chức năng chỉ được coi là hoàn thành khi:

- Có giao diện sử dụng thực tế.
- Có API/backend và validation nếu nghiệp vụ cần.
- Có lưu trữ dữ liệu thật.
- Có xử lý quyền.
- Có xử lý lỗi.
- Có test hoặc bằng chứng kiểm thử phù hợp.
- Có cập nhật tài liệu.
- Không tạo tác dụng phụ sai đối với tồn kho, công nợ, doanh thu hoặc dữ liệu liên quan.

Tiêu chí nghiệm thu toàn hệ thống:

1. Quản lý được sản phẩm của ba nhãn hàng.
2. Theo dõi được tồn kho theo SKU, kho, lô và hạn sử dụng.
3. Theo dõi được hàng đang nằm tại từng nhân viên.
4. Quản lý được đơn hàng của năm kênh bán.
5. Theo dõi được đổi trả, hàng hỏng và hàng hết hạn.
6. Theo dõi được đại lý, khách hàng và công nợ.
7. Quản lý được thu tiền hộ và đối soát nhân viên.
8. Tính được báo cáo doanh thu, giá vốn, lợi nhuận và chi phí theo quy tắc rõ ràng.
9. Quản lý được chấm công, nghỉ phép, lương, thưởng và KPI.
10. Phân quyền đúng cả frontend lẫn backend.
11. Có audit log và phương án sao lưu.
12. Có hướng dẫn cài đặt, triển khai và vận hành.
13. Các kiểm thử quan trọng đã chạy hoặc có báo cáo chính xác về giới hạn chưa kiểm thử.

---

## 21. Kết quả đầu ra bắt buộc

Sau khi khảo sát, hãy tạo hoặc cập nhật các tài liệu:

- `docs/ERP_AUDIT.md`
- `docs/ERP_IMPLEMENTATION_PLAN.md`
- `docs/ERP_DATA_MODEL.md`
- `docs/ERP_BUSINESS_RULES.md`
- `docs/ERP_TEST_REPORT.md`
- `docs/ERP_DEPLOYMENT.md`

Điều chỉnh đường dẫn nếu repository có quy ước tài liệu khác.

Trong báo cáo cuối cùng, liệt kê:

1. Kiến trúc và công nghệ hiện tại.
2. Các chức năng đã có trước khi sửa.
3. Các chức năng đã bổ sung hoặc sửa.
4. Những file quan trọng đã thay đổi.
5. Các migration database đã tạo.
6. Các lệnh đã chạy.
7. Kết quả test thực tế.
8. Các chức năng chưa hoàn thiện.
9. Các giả định nghiệp vụ đã sử dụng.
10. Các biến môi trường cần cấu hình, chỉ nêu tên biến, không hiển thị bí mật.
11. Hướng dẫn chạy local và deploy online.
12. Cách sao lưu và khôi phục dữ liệu.
13. Các rủi ro hoặc quyết định còn cần người dùng xác nhận.

Không tuyên bố hoàn thành những chức năng mới chỉ có giao diện hoặc chưa được kiểm thử.

## 22. Chỉ thị bắt đầu

Bắt đầu bằng việc khảo sát repository hiện tại.

Bước đầu tiên, hãy xác định cấu trúc dự án, công nghệ, database, các module đã có và các lệnh kiểm thử hiện có. Sau đó lập tài liệu khảo sát và kế hoạch triển khai.

Tiếp theo, thực hiện những thay đổi có thể xác định rõ từ yêu cầu trên, theo từng phase, ưu tiên tính toàn vẹn dữ liệu và khả năng vận hành thực tế.

Nếu phát hiện chức năng hiện tại đã đáp ứng yêu cầu, hãy giữ nguyên hoặc cải thiện có chọn lọc thay vì viết lại.

Nếu phát hiện yêu cầu chưa đủ rõ để quyết định một thay đổi có rủi ro cao, hãy nêu câu hỏi, đưa ra phương án đề xuất và chờ xác nhận trước khi thực hiện thay đổi đó.

Mục tiêu cuối cùng là nâng cấp thành công repository hiện tại thành hệ thống ERP có thể sử dụng thực tế cho doanh nghiệp phân phối thực phẩm bảo vệ sức khỏe, với dữ liệu chính xác, phân quyền an toàn, báo cáo đối soát được và khả năng mở rộng trong tương lai.