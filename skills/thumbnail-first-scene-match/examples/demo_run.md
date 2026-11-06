# Ví dụ vận hành v2.3: NO TEXT + FEEDBACK, gốc cây khổng lồ đang trên xe

**Đầu vào:** ảnh gốc cây có mặt cắt nứt lớn đang nằm/treo ở nhà máy; mục tiêu là ảnh bìa có xe chở cây cực kỳ khổng lồ. **Khán giả quốc tế, không có text trên ảnh.**

**Tạo 4 ảnh PNG riêng:**
- `A.png`: camera thấp sau trái; mặt cắt lớn sát máy; nhìn thấy đầu kéo, trailer siêu dài ở xa.
- `B.png`: góc cao toàn đoàn xe vào sân xưởng; cabin, trailer, cây cùng hiện rõ, worker nhỏ.
- `C.png`: góc ngang thấp bên hông để thấy 14+ bánh (không cần đếm/ghi số), hệ đỡ & dây chằng; cảnh vận chuyển chậm.
- `D.png`: camera trước 3/4, đầu kéo tiến vào cửa xưởng, thân cây to khủng bố phía sau.

**Tất cả:** 16:9, không chữ/biển số đọc được/nhãn/logo/mũi tên/số đo, không collage; giữ đúng đặc trưng cây gốc, cây được **xe chở thật**.

**Evidence:** ảnh người dùng chứng minh tính chất khúc gỗ nhưng KHÔNG chứng minh đã từng có cảnh xe vận tải; xe chở là `ai_reconstruction`. Video nếu chưa có: `SCENE_MATCH_PENDING`.

**Reject trước giao:** chỉ có cẩu treo, không có cabin, gỗ đổi thành slab, 4 ảnh chỉ khác crop hoặc xe đỏ cùng góc, một ảnh có text “D-08” hoặc “L=12.8m”, bất kỳ infographic.

**Scene-match:** chỉ khi người dùng cung cấp dựng được một shot nhận ra đúng xe+gỗ, xác minh nội dung và provenance, mới có thể thông báo chèn cảnh thành công.

**Retention:** đăng ký bản sao preview local để auto-clean sau 5h; không xóa ảnh gốc hoặc đã xuất.
