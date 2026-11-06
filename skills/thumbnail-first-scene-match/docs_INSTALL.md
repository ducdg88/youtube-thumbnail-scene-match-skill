# HƯỚNG DẪN CÀI VÀ DÙNG (CLAUDE / CLAUDE CODE)

## Chỉ thả ZIP vào chat đã tự kích hoạt Skill chưa?

**Chưa.** Claude có thể đọc file đính kèm trong một cuộc chat theo yêu cầu, nhưng đó không đồng nghĩa với việc cài Skill dùng lâu dài.

### Claude.ai

1. Giải nén không bắt buộc. Dùng ZIP có thư mục gốc `thumbnail-first-scene-match/` chứa `SKILL.md`.
2. Vào **Customize > Skills > + > Create skill > Upload a skill** (tên nút có thể thay đổi theo UI).
3. Tải ZIP lên, bật Skill.
4. Trong cuộc chat mới, chỉ cần gửi ảnh/video và yêu cầu “Cho xe chở gốc cây này, cực kỳ khổng lồ, làm 4 thumbnail”; Claude sẽ **xem mô tả Skill để chọn dùng khi phù hợp**. Không bảo đảm chọn đúng 100%; nếu không dùng, chỉ rõ tên `thumbnail-first-scene-match`.
5. Bật **code execution** nếu hệ thống yêu cầu. Để feedback tích lũy qua các cuộc chat, giữ/download tệp feedback riêng rồi tải lại hoặc dùng môi trường lưu file lâu dài; Skill không tự sửa bản ZIP đã cài.

### Claude Code

Giải nén để đúng đường dẫn project `.claude/skills/thumbnail-first-scene-match/SKILL.md` hoặc trong thư mục cá nhân `~/.claude/skills/thumbnail-first-scene-match/SKILL.md`. Khởi động phiên mới để Claude đọc metadata và tự chọn dùng theo yêu cầu. Các thư mục dữ liệu runtime cần nằm ngoài thư mục ZIP và vault preview xóa sau 5h.

## Feedback loop cụ thể (Python 3.9+, stdlib)

```bash
python scripts/feedback_loop.py init
python scripts/feedback_loop.py record --run-id video-001 --concept A --decision revise --issue too_small --scale-level 3 --story log_truck_yard --notes "cây còn nhỏ"
python scripts/feedback_loop.py record --run-id video-001 --concept B --decision selected --scale-level 3 --story full_convoy_arrival --rating 5
python scripts/feedback_loop.py recommend --current-scale 3
```

Vòng lặp này lưu feedback vào `~/.thumbnail_first_scene_match/feedback/feedback.json` hoặc biến môi trường `THUMBNAIL_FEEDBACK_FILE`. Kết quả ví dụ đề xuất tăng scale 3→4, ưu tiên nguyên tắc bố cục đã được user lựa chọn nhưng vẫn phải tạo các concept mới khác biệt, không sao chép nguyên mẫu.

**Quan trọng:** Nếu Claude không có filesystem bền vững giữa các cuộc chat, người dùng/agent phải xuất và tải lại file JSON để duy trì lịch sử. Đây là cải tiến theo lần tương tác, không phải tác vụ chạy ngầm liên tục.
