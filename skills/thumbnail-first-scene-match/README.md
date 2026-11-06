# Thumbnail First > Scene Match Skill v2.3: TỰ NHẬN DIỆN + FEEDBACK LOOP

Được cập nhật theo các yêu cầu trong phiên làm việc: **thumbnail cho kênh quốc tế > TUYỆT ĐỐI KHÔNG TEXT / LOGO / SỐ ĐO trên ảnh**, mỗi lần trả **3-5 thumbnail 16:9 (mặc định 4)**, đúng gốc cây từ ảnh tham chiếu, cực kỳ khổng lồ và **thật sự được xe đầu kéo cùng trailer đa trục chở**. Các concept khác nhau thực chất; chèn cảnh tương ứng vào video chỉ khi có nguồn/đầu ra có thể kiểm chứng.

**Đọc theo thứ tự:** `SKILL.md` > `profile/SESSION_CREATIVE_BRIEF.md` > `profile/creative_profile.json` > `templates/NO_TEXT_BATCH_PROMPTS.md`.

### Cách gọi trong agent

> Dùng Skill `thumbnail-first-scene-match` v2.3. Theo creative brief của phiên này, tạo 4 **ảnh** thumbnail riêng 16:9 hoàn toàn không chữ, không logo, cùng gốc cây trong ảnh tham chiếu được xe siêu trường siêu trọng mang trên trailer; bốn câu chuyện và góc camera khác nhau. QA từng ảnh; lập kế hoạch Scene Match và quản lý preview 5 giờ theo điều kiện local.

### Bảo vệ preview cục bộ sau 5 giờ

`preview_vault.py` (Python 3.9+, stdlib) lưu bản sao preview trong vault riêng và xóa sau 5 giờ khi công việc cleanup thực sự chạy. Không xóa ảnh gốc.

```sh
python scripts/preview_vault.py register "path/to/thumbnail_A.png" --concept A
python scripts/preview_vault.py register "path/to/thumbnail_B.png" --concept B
python scripts/preview_vault.py status
python scripts/preview_vault.py cleanup
python tests/test_preview_vault.py
```

Mặc định vault: `~/.thumbnail_first_scene_match/private_previews`; đặt biến `THUMBNAIL_VAULT_DIR` để đổi vị trí.

Trên Windows (PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_windows_cleanup.ps1
```

Task Scheduler dọn **mỗi 5 phút**, TTL từng ảnh = **5 giờ**; việc dọn yêu cầu máy hoạt động và task hợp lệ. Không có khả năng xóa ảnh trong ChatGPT/CDN/thiết bị khác hoặc ngăn copy trong 5 giờ. Các ảnh duyệt cần giữ phải xuất ra thư mục riêng trước khi xóa preview.

### Kiểm tra kỹ thuật batch

```sh
pip install pillow
python scripts/batch_qc.py thumbnail_A.png thumbnail_B.png thumbnail_C.png thumbnail_D.png
```

`batch_qc.py` chỉ kiểm tra tỷ lệ ảnh và near-duplicate ở mức pixel. **KHÔNG tự xác thực được ảnh không chữ, có xe chở, tính mới hay việc tuân thủ YouTube**; agent phải mở ảnh, kiểm tra nội dung và chịu trách nhiệm ghi rõ trạng thái kiểm tra thủ công. Nếu chỉ có ảnh mà chưa có video > `SCENE_MATCH_PENDING`, không tự báo đã chèn MP4.


## MỚI TRONG v2.2

- Thêm tham số **Size Amplification** để người dùng chỉnh mức phóng đại kích thước gốc cây ở các lần sau.
- Mặc định level 3; hỗ trợ level 1-5.
- Có thể giữ nguyên concept và chỉ tăng scale nếu người dùng yêu cầu “to hơn nữa”.


## v2.3: AUTO RECOGNITION + FEEDBACK LOOP

- **Cài đúng:** Claude.ai Customize > Skills > `+` > Create skill > Upload a skill. ZIP chứa thư mục gốc `thumbnail-first-scene-match/` khớp frontmatter `name:`. Bật Skill và code execution nếu được yêu cầu. **Chỉ đính kèm ZIP trong chat không cài Skill.**
- **Tự nhận diện sau khi cài:** gửi ảnh/video và nói “làm 4 thumbnail, cho xe chở gốc cây khổng lồ”, không cần nhắc Skill theo tên. Việc gọi tự động phụ thuộc agent phân loại nhiệm vụ, không cam kết luôn kích hoạt.
- **Feedback loop có thể lưu:** sau mỗi lượt user chọn/chê/sửa, ghi feedback JSON; lần sau tổng hợp để điều chỉnh scale, loại lỗi đã gặp và bố cục. Không học ngầm khi không có tương tác hoặc nơi lưu bền vững.
- **Hướng dẫn:** xem `docs_INSTALL.md` và `profile/AUTO_RECOGNITION_AND_FEEDBACK.md`.

```bash
python scripts/feedback_loop.py init
python scripts/feedback_loop.py record --run-id demo1 --concept A --decision revise --issue too_small --scale-level 3
python scripts/feedback_loop.py recommend --current-scale 3
python tests/test_feedback_loop.py
```
