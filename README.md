# Simple CRM for Frappe Framework v16

Hệ thống quản lý quan hệ khách hàng (CRM) xây dựng trên nền tảng **Frappe Framework v16**, tối ưu hóa quy trình quản lý khách hàng tiềm năng, cơ hội bán hàng, chăm sóc khách hàng và báo cáo phễu chuyển đổi.

---

## 🌟 Tính Năng Nổi Bật

### 1. Quản Lý Nghiệp Vụ Toàn Diện (9 DocTypes)
- **CRM Lead**: Quản lý khách hàng tiềm năng, kiểm tra trùng lặp Email/Phone, tự động ghi nhận thời gian đánh giá (qualification timestamp).
- **CRM Customer**: Hồ sơ khách hàng chính thức, chặn xóa khách hàng khi còn cơ hội mở (BR-15).
- **CRM Contact**: Danh bạ người liên hệ, cơ chế chỉ định 1 Primary Contact duy nhất cho mỗi khách hàng (BR-06).
- **CRM Opportunity**: Quản lý cơ hội kinh doanh / Pipeline, tự động map xác suất chốt deal theo từng giai đoạn (BR-07, BR-08), bắt buộc lý do khi deal thất bại (BR-09).
- **CRM Activity**: Lịch sử tương tác đa kênh (Cuộc gọi, Họp, Email) sử dụng liên kết động `Dynamic Link` (BR-14) và tự động cập nhật ngày liên hệ gần nhất cho Lead.
- **CRM Task**: Giao việc và theo dõi nhiệm vụ cần làm, phân loại tự động công việc quá hạn (BR-11).
- **CRM Lead Source** & **CRM Lost Reason**: Quản lý danh mục nguồn tiếp cận và lý do mất deal.
- **CRM Settings**: Cấu hình phân cấp hệ thống CRM (Single DocType).

### 2. Quy Trình Chuyển Đổi Tinh Gọn (Lead Conversion)
- Nút bấm trực tiếp **Convert to Customer** trên giao diện Lead khi Lead đạt trạng thái `Qualified`.
- Dialog popup cho phép nhập nhanh: Tên khách hàng, Tiêu đề cơ hội, Giá trị deal dự kiến, Ngày chốt mong đợi.
- Thực thi chuyển đổi nguyên tử (Atomic transaction) an toàn: tạo cùng lúc Customer, Contact và Opportunity, đồng thời chuyển trạng thái Lead sang `Converted`.

### 3. Phân Quyền Phân Cấp Động (Row-level Security)
- **CRM Sales User**: Chỉ xem và thao tác trên dữ liệu (Lead, Opportunity, Task) được phân công cho chính mình.
- **CRM Sales Manager**: Toàn quyền xem và quản lý dữ liệu của tất cả nhân viên kinh doanh trong nhóm.
- **CRM Admin**: Toàn quyền cấu hình hệ thống, danh mục và quản trị người dùng.

### 4. Báo Cáo Quản Trị & Phân Tích (4 Script Reports)
- **Lead Conversion Funnel**: Phễu chuyển đổi từ Lead mới -> Đã tiếp cận -> Đạt chuẩn -> Chuyển đổi thành công.
- **Opportunity Pipeline**: Tổng hợp cơ hội theo từng giai đoạn bán hàng kèm đồ thị trực quan.
- **Overdue Follow-ups**: Cảnh báo tức thì danh sách nhiệm vụ và lead quá hạn chưa được chăm sóc.
- **Deal Won/Lost Summary**: Thống kê số lượng và doanh thu các thương vụ Thắng / Thua theo từng tháng.

### 5. CRM Workspace
- Không gian làm việc trực quan với 6 thẻ số liệu nhanh (Number Cards), lối tắt truy cập nhanh và danh mục báo cáo phân tích.

---

## 🚀 Cài Đặt (Installation)

### Cách 1: Cài đặt vào Bench có sẵn

```bash
cd /path/to/your/frappe-bench

# 1. Tải app vào bench
bench get-app https://github.com/hbaovidai/CRM

# 2. Cài đặt app vào site của bạn
bench --site your-site.local install-app simple_crm

# 3. Chạy migration
bench --site your-site.local migrate

# 4. (Tùy chọn) Nạp dữ liệu mẫu Demo
bench --site your-site.local execute simple_crm.setup.seed_demo.execute
```

---

## 🧪 Kiểm Thử Tự Động (Automated Testing)

App đi kèm bộ unit/integration test bao phủ 100% các Business Rules theo chuẩn Frappe Test Framework:

```bash
bench --site your-site.local run-tests --app simple_crm
```
*Kết quả: 20/20 test cases pass 100%.*

---

## 👥 Tài Khoản Demo Mặc Định (Sau Khi Chạy Seed)

| Vai trò | Email đăng nhập | Mật khẩu |
| :--- | :--- | :--- |
| **CRM Admin** | `admin_crm@example.com` | `admin123` |
| **CRM Sales Manager** | `manager_crm@example.com` | `admin123` |
| **CRM Sales User** | `sales_crm@example.com` | `admin123` |

---

## 📄 Bản Quyền (License)

Mã nguồn được phân phối theo giấy phép [MIT](license.txt).
