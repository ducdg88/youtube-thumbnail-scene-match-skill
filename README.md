# Thumbnail First, Scene Match: skill thumbnail YouTube không chữ cho kênh nước ngoài

**Tiếng Việt** | [English](README.en.md)

![CI](https://github.com/ducdg88/youtube-thumbnail-scene-match-skill/actions/workflows/validate.yml/badge.svg) ![license](https://img.shields.io/badge/license-MIT-green) ![version](https://img.shields.io/badge/version-2.3.0-blue)

Agent Skill (file `SKILL.md`) giúp AI làm **thumbnail YouTube không chữ** cho kênh hướng tới khán giả quốc tế: mỗi lượt ra 3 đến 5 ảnh 16:9 riêng (mặc định 4), mỗi ảnh một câu chuyện và một góc máy khác nhau, giữ đúng chủ thể trong ảnh tham chiếu, rồi lên kế hoạch chèn cảnh tương ứng vào video (Thumbnail First, Scene Match). Có vòng phản hồi: bạn chọn hay chê ảnh nào, skill ghi lại để lần sau làm tốt hơn. Dùng được với Claude, Claude Code và mọi agent đọc `SKILL.md`. Do [DUCPT](https://ducpt.com/?utm_source=github&utm_medium=readme&utm_campaign=youtube-thumbnail-scene-match-skill) làm và dùng thật cho kênh của mình.

Bộ mẫu sẵn trong skill là ngách **xe siêu trường chở gốc cây khổng lồ**; bạn đổi brief trong `profile/` cho ngách của mình.

## Skill làm gì

- **Không chữ, không logo, không số đo trên ảnh.** Khán giả quốc tế hiểu bằng hình, không cần dịch. Tên A, B, C, D chỉ nằm ở tên file.
- **3 đến 5 ảnh riêng, 16:9**, không ghép collage, không thay ảnh bằng prompt hay mô tả.
- **Khác nhau thật sự**: mỗi ảnh khác ít nhất 3 điểm, bắt buộc khác câu chuyện và khác góc máy; đổi màu hay cắt khung không tính.
- **Giữ đúng chủ thể** của ảnh tham chiếu (hình mặt cắt, vết nứt, vỏ, màu gỗ).
- **Thang phóng đại 1 đến 5**: nói "to hơn nữa" hay "scale level 4" là skill tăng cảm giác khổng lồ bằng góc máy, người nhỏ, xe dài, không bịa số đo.
- **Scene Match trung thực**: thumbnail hứa gì thì video phải có cảnh đó. Chưa có video thì ghi `SCENE_MATCH_PENDING`, không báo đã chèn.
- **Vòng phản hồi**: ghi lựa chọn và lỗi (`too_small`, `same_concept`, `text_logo`, `missing_truck`), lần sau đề xuất điều chỉnh, nhưng không bao giờ phá luật cứng.
- **Ảnh xem thử tự xoá sau 5 giờ**: chỉ bản sao trong kho riêng của skill, không đụng ảnh gốc hay ảnh đã duyệt.

## Cài đặt

**Claude.ai**: vào Customize, Skills, `+`, Create skill, Upload a skill. Nén thư mục `skills/thumbnail-first-scene-match` thành ZIP (thư mục gốc trong ZIP phải tên `thumbnail-first-scene-match`), tải lên và bật. Chỉ đính kèm ZIP vào cuộc chat thì chưa phải cài.

**Claude Code**:

```bash
git clone https://github.com/ducdg88/youtube-thumbnail-scene-match-skill.git
cp -r youtube-thumbnail-scene-match-skill/skills/thumbnail-first-scene-match ~/.claude/skills/
pip install pillow   # cho batch_qc.py
```

Agent khác đọc `SKILL.md`: chép thư mục đó vào thư mục skills của agent. Mở phiên mới để skill được nhận.

## Cách dùng

Sau khi cài, gửi ảnh hoặc video và nói tự nhiên, không cần gọi tên skill:

> Cho xe chở gốc cây này, cực kỳ khổng lồ, làm 4 thumbnail.

Hoặc gọi rõ:

> Dùng skill `thumbnail-first-scene-match`. Tạo 4 thumbnail 16:9 không chữ, không logo, cùng gốc cây trong ảnh tham chiếu được xe chở trên trailer nhiều trục; bốn câu chuyện và góc máy khác nhau. QA từng ảnh và lập kế hoạch Scene Match.

Lượt sau chỉ cần nhận xét: "cây còn nhỏ", "ảnh B đẹp nhất", "các ảnh giống nhau", "có chữ trên ảnh". Skill ghi phản hồi và sửa đúng chỗ, không tự làm lại cả bộ.

Skill cần **máy tạo ảnh AI** của agent để ra ảnh thật. Không có thì skill nói rõ, không giả vờ đã có ảnh.

## Skill làm việc thế nào

1. Đọc `config/defaults.json`, brief trong `profile/` và phản hồi lần trước.
2. Phân tích ảnh, video nguồn, lập sổ bằng chứng: cảnh nào quay thật (`real_verified`), cảnh nào AI dựng lại (`ai_reconstruction`).
3. Chọn 3 đến 5 ý tưởng khác câu chuyện và góc máy (mẫu A cận mặt cắt từ đuôi xe, B toàn đoàn xe vào xưởng, C ngang hông thấy dãy trục, D đầu kéo vào cổng, E chuẩn bị dỡ hàng).
4. Tạo từng ảnh với prompt chặn chữ luôn bật (`templates/NO_TEXT_BATCH_PROMPTS.md`).
5. QA từng ảnh: đúng chủ thể, đủ khổng lồ, xe chở thật, 16:9, không chữ; so trùng giữa các ảnh.
6. Giao ảnh, giải thích khác biệt trong lời nhắn (không viết lên ảnh), bạn chọn hoặc yêu cầu sửa.
7. Ghép ảnh đã chọn với một cảnh tương ứng trong video, có nguồn và timecode.

## Script đi kèm

```bash
# kiểm tỉ lệ 16:9 và ảnh gần trùng (chỉ kiểm kỹ thuật, vẫn phải xem bằng mắt)
python skills/thumbnail-first-scene-match/scripts/batch_qc.py A.png B.png C.png D.png

# kho ảnh xem thử tự xoá sau 5 giờ (mặc định ~/.thumbnail_first_scene_match/private_previews, đổi bằng THUMBNAIL_VAULT_DIR)
python skills/thumbnail-first-scene-match/scripts/preview_vault.py register A.png --concept A
python skills/thumbnail-first-scene-match/scripts/preview_vault.py status
python skills/thumbnail-first-scene-match/scripts/preview_vault.py cleanup

# vòng phản hồi (mặc định ~/.thumbnail_first_scene_match/feedback/feedback.json, đổi bằng THUMBNAIL_FEEDBACK_FILE)
python skills/thumbnail-first-scene-match/scripts/feedback_loop.py init
python skills/thumbnail-first-scene-match/scripts/feedback_loop.py record --run-id video-001 --concept A --decision revise --issue too_small --scale-level 3
python skills/thumbnail-first-scene-match/scripts/feedback_loop.py recommend --current-scale 3
```

Trên Windows, cài lịch dọn ảnh xem thử mỗi 5 phút (chạy bằng `pythonw.exe` nên không nháy cửa sổ):

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\thumbnail-first-scene-match\scripts\install_windows_cleanup.ps1
```

Kiểm thử: `python skills/thumbnail-first-scene-match/tests/test_skill_contract.py` (và `test_preview_vault.py`, `test_feedback_loop.py`).

## Đổi sang ngách của bạn

Bộ mẫu viết cho xe chở gốc cây. Để dùng cho ngách khác, sửa 3 chỗ:
- `profile/SESSION_CREATIVE_BRIEF.md`: mục tiêu hình ảnh, chủ thể bắt buộc, lỗi từng gặp.
- `profile/creative_profile.json`: `required_scene`, `not_allowed`, đặc điểm chủ thể cần giữ.
- `templates/NO_TEXT_BATCH_PROMPTS.md`: câu ràng buộc chung và 4 đến 5 ý tưởng mẫu.

Luật không chữ, 16:9, ảnh riêng, khác câu chuyện và góc máy, Scene Match trung thực dùng được cho mọi ngách.

## Giới hạn

- `batch_qc.py` chỉ kiểm tỉ lệ và trùng điểm ảnh; không tự biết ảnh có chữ hay chủ thể đúng chưa. Phải xem bằng mắt.
- Skill không đảm bảo tránh khiếu nại hay đạt YouTube Partner Program; nội dung video vẫn phải có giá trị riêng. Cảnh AI dựng lại giống thật cần cân nhắc khai báo nội dung tổng hợp trong YouTube Studio.
- Không xoá được ảnh đã nằm trên dịch vụ chat hay thiết bị khác; chỉ dọn kho xem thử trên máy.
- Phản hồi chỉ được nhớ qua các phiên khi có nơi lưu file lâu dài.

## Về DUCPT

[DUCPT](https://ducpt.com/?utm_source=github&utm_medium=readme&utm_campaign=youtube-thumbnail-scene-match-skill) làm công cụ AI, quy trình tự động và đào tạo cho người làm nội dung, kênh YouTube và doanh nghiệp nhỏ ở Việt Nam:

- [DUCPT Skills](https://ducpt.com/skills/?utm_source=github&utm_medium=readme&utm_campaign=youtube-thumbnail-scene-match-skill): bộ Agent Skill miễn phí cho người làm một mình với AI
- [YouTube Title Lab](https://ducpt.com/skills/youtube-title-lab/?utm_source=github&utm_medium=readme&utm_campaign=youtube-thumbnail-scene-match-skill): skill viết và chấm tiêu đề YouTube, đi cặp với thumbnail
- [Tìm Nguồn YouTube](https://ducpt.com/dich-vu/tim-nguon-youtube?utm_source=github&utm_medium=readme&utm_campaign=youtube-thumbnail-scene-match-skill): tìm nguồn video cho kênh
- [Tab Cộng Đồng AI](https://ducpt.com/cong-cu-ai/tab-cong-dong-ai?utm_source=github&utm_medium=readme&utm_campaign=youtube-thumbnail-scene-match-skill): viết bài Cộng đồng YouTube bằng AI
- [Khoá học](https://ducpt.com/khoa-hoc/?utm_source=github&utm_medium=readme&utm_campaign=youtube-thumbnail-scene-match-skill): làm kênh và vận hành doanh nghiệp bằng AI

Skill làm bộ nhận diện kênh (logo, ảnh đại diện, ảnh bìa): [youtube-channel-branding-skill](https://github.com/ducdg88/youtube-channel-branding-skill).

## Giấy phép

[MIT](LICENSE).
