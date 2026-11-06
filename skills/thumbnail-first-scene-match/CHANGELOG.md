## v2.3.0
- Added auto-recognition metadata and triggers for installed/enabled Skill workflows.
- Fixed Claude upload root directory to match `name: thumbnail-first-scene-match`.
- Added event-sourced feedback loop, adaptive scale suggestions, issue taxonomy and story signals (explicit user feedback only).
- Feedback journal is outside expiring 5-hour previews; no background learning/remote deletion implied.
- Added tests and install guide, updated v2.1 stale test contract.

## v2.2.0
- Added user-editable `size_amplification` parameter (levels 1-5).
- Updated skill contract so future requests like “to hơn nữa” can be handled without rewriting the workflow.
- Updated prompt builders, defaults, creative profile, and session brief.

# Changelog

## v2.1.0: International / NO TEXT (2026-11-06)
- Mặc định **không có text, chữ, số, logo, watermark, chú thích hoặc dữ liệu kích thước** trên mọi thumbnail; tên concept chỉ đặt ngoài ảnh.
- Thêm creative profile rút từ nhiều lần người dùng yêu cầu/chỉnh ảnh trong phiên: cây gốc cực kỳ khổng lồ, giữ đúng mặt cắt/vết nứt/vỏ, xe đầu kéo + trailer nhiều trục PHẢI thật sự đang chở gốc cây.
- Chặn các lỗi đã gặp: chỉ có slab, gốc cây treo cẩu thay vì trên xe, collage quảng bá, 4 ảnh cùng một mô-típ, text số đo giả.
- Củng cố yêu cầu 3-5 ảnh riêng 16:9, mặc định 4, concept khác action + camera.
- Thêm bộ prompt NO TEXT, creative_profile.json, manifest ví dụ và quality tests; QC kỹ thuật không giả định có thể tự nhận diện text hoặc xác minh hình ảnh/footage.
- Giữ nguyên TTL local 5h và quy tắc Scene Match trung thực.

## v2.0.0
- Batch 3-5 ảnh, preview vault TTL 5h, scene-match evidence planning, QC kỹ thuật.
