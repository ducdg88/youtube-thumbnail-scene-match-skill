# BRIEF RÚT RA TỪ CÁC YÊU CẦU TRONG PHIÊN LÀM VIỆC

Tài liệu này là **đặc tả sáng tạo** để agent hiểu yêu cầu thực tế. Không phải tuyên bố về dữ liệu kênh, lịch sử xuất bản hoặc quyền sở hữu tài liệu.

## Mục tiêu hình ảnh

- Dành cho **khán giả quốc tế**: chỉ truyền tải thông điệp bằng hình ảnh, **KHÔNG có bất kỳ chữ, số hay ký hiệu chú thích được thêm vào thumbnail**. Không thêm tiêu đề tiếng Anh chỉ vì khán giả nước ngoài. Không thêm logo, watermark hay tên kênh. Không đưa bảng giải thích quy trình vào ảnh.
- Hook thị giác tức thì: **gốc cây siêu khổng lồ** chiếm ưu thế; quy mô gần như phi thường nhưng chất liệu, ánh sáng, vật lý và vận tải trông như cảnh quay tài liệu thật.
- Thông điệp bắt buộc: **xe đang chở gốc cây**, không phải chỉ có cây lớn trong sân gỗ, hay cây treo bằng cẩu ngay phía trên xe. Cần nhìn ra cabin, trailer nhiều trục, bánh xe và cấu trúc kê/chằng.
- Đối chiếu người nhỏ, bánh xe, cổng xưởng, nhà máy để người xem cảm thấy quy mô. Tránh phải đoán kích cỡ nhờ số liệu trên ảnh.
- Duy trì nhận diện đúng thân cây từ ảnh gốc: đầu cắt bất đối xứng, rạn nứt cũ, vỏ sẫm thô, chất gỗ nâu/đen, dáng gốc và độ thuôn. Không thay thành slab bóng hoặc mặt cắt vân xoáy nhuộm màu.
- 16:9, ảnh sắc nét, tương phản dễ đọc khi thu nhỏ, góc máy điện ảnh công nghiệp; ánh sáng tự nhiên / HDR vừa phải, không biến thành đồ họa ảo.

## Những lần người dùng đã chỉnh lại: coi là bài học ưu tiên cao

1. **“Cho xe chở: tôi nhấn mạnh là cho xe chở gốc cây khổng lồ này.”** Vì từng có ảnh tập trung vào gỗ/slab mà thiếu xe. Không chấp nhận thiếu xe vận tải.
2. **“Cực kỳ khổng lồ”** là yêu cầu quan trọng nhất về ấn tượng thị giác; tuy nhiên không được bịa chiều dài, đường kính, tuổi cây hoặc tải trọng.
3. **“Tỷ lệ 16:9.”** Xuất từng ảnh độc lập tỷ lệ 16:9, không thay bằng poster/collage/infochart có nhiều thumbnail.
4. **“3-5 ảnh mỗi lần.”** Mặc định trả 4 ảnh hoàn chỉnh, concept khác nhau về chuyện đang xảy ra *và* góc máy, không phải một mẫu xe đỏ đổi crop.
5. **“Không cần ghi text, bỏ text đi.”** Áp dụng với mọi thế hệ ảnh: cấm chữ/số ngay trên vật thể, cabin, đầu gỗ, nền, kể cả số đo AI tự thêm. Tên file A/B/C/D nằm bên ngoài ảnh.
6. **“Thumbnail trước, cảnh video tương ứng sau.”** Không chỉ ghép ảnh tĩnh vào một footage không liên quan. Cần shot cùng chủ thể/hành động, kiểm tra timecode, ghi rõ là tái dựng AI khi đúng như vậy.
7. **“Tránh mẫu lặp và spam.”** Đổi hook, diễn biến, góc nhìn, nguồn footage và giá trị thuyết minh/biên tập; không nghĩ chỉ xóa chữ hay đổi màu là đủ tuân thủ YouTube.
8. **“Tự xóa sau 5 giờ.”** Chỉ tự xóa các **bản preview được quản lý cục bộ**; không hứa xóa ảnh chat hoặc các bản sao bên ngoài.

## Các lựa chọn có thể tạo khác biệt thực sự

- Tập trung đầu cắt vs toàn đoàn xe, góc từ mặt đất vs từ cao, xe vào xưởng vs dừng cân bằng/chằng buộc, đường nội bộ vs bãi vận tải; chỉ chọn hành động có thể đối chiếu video/cảnh dựng được phê duyệt.
- Không cố định mọi ảnh là xe màu đỏ, cùng góc sau 3/4, cùng công nhân áo xanh. Màu phương tiện là phụ; **câu chuyện hình ảnh mới** là chính.
- Khi thiếu video gốc có cảnh xe chở, đánh dấu `AI_RECONSTRUCTION` và `SCENE_MATCH_PENDING` cho đến khi có cảnh video thực sự tương ứng.

## Phân loại yêu cầu

- **MUST:** ảnh không chữ; gốc cây gốc/đúng đặc trưng; cực kỳ to; được xe đầu kéo + rơ-moóc chở thật; 16:9; 3-5 ảnh riêng; bối cảnh đáng tin; có chuẩn Scene Match.
- **SHOULD:** công nhân nhỏ đối tỷ lệ, nhiều trục rõ, mặt đầu gỗ nổi bật, tông ảnh công nghiệp điện ảnh, ánh sáng rõ, không dính nhãn thương hiệu.
- **MUST NOT:** chỉ cẩu treo, chỉ gỗ không xe, poster có text, bảng infographic, đồ gỗ thành phẩm khi yêu cầu là vận tải, chỉ thay màu/crop, tự nhận có footage bằng chứng khi chưa có.

9. Người dùng muốn có thể tăng kích thước cây ở các lần sau; Skill phải cho phép chỉnh **mức phóng đại kích thước** thay vì cố định một scale.

10. User muốn ZIP cài một lần để agent tự nhận diện đúng các yêu cầu thumbnail khi được bật; dùng feedback sau mỗi lựa chọn/sửa ảnh để cải tiến các vòng sau. Việc cải tiến chỉ tồn tại qua phiên khi có file state lâu dài, không chạy ngầm.
