# AUTO RECOGNITION + FEEDBACK LOOP: v2.3

## Nhận diện khi nào dùng Skill

**Sau khi người dùng cài và bật Skill trong công cụ hỗ trợ Skills**, hãy sử dụng Skill khi yêu cầu phù hợp với một trong các nhóm sau:

- Người dùng tải ảnh/video gốc cây gỗ lên và yêu cầu tạo, sửa hoặc phóng đại **thumbnail YouTube** về xe chở cây khổng lồ.
- Người dùng nói “cho xe chở cây này”, “cực kỳ khổng lồ”, “tạo ảnh bìa”, “làm 3-5 thumbnail”, “làm thumbnail từ video này”, hoặc nhắc tới **Thumbnail First > Scene Match**.
- Người dùng muốn hình bìa giống một cảnh có trong video, muốn đánh giá các phương án thumbnail, hoặc muốn tiếp tục chỉnh một ảnh đã chọn.
- Người dùng nói “cây còn nhỏ”, “tăng scale lên 5”, “mẫu B đẹp hơn”, “ảnh bị chữ”, “ảnh trùng nhau”: đó là **feedback kích hoạt vòng cải tiến**, không phải lệnh mặc định tạo lại cả bộ nếu user chỉ đưa nhận xét.

**Không nên tự kích hoạt** trên mọi ảnh bất kỳ không liên quan đến thumbnail/video, không đánh đồng việc đọc file ZIP với việc đã cài đặt Skill, không tự chạy lệnh nền khi không có phiên làm việc hoặc scheduler.

**Ưu tiên tác vụ cụ thể mới nhất** nếu mâu thuẫn với mặc định mềm. Những ràng buộc bất biến (NO TEXT / 16:9 / truck actually carries log / proven scene match / no fictional facts) chỉ thay đổi với yêu cầu rõ ràng của người dùng và vẫn cần tuân thủ chính sách nền tảng.

## Thứ tự bắt buộc mỗi lần chạy

1. Đọc `config/defaults.json`, `profile/creative_profile.json`, `profile/SESSION_CREATIVE_BRIEF.md` và **báo cáo feedback lần trước** (nếu có). Không đoán rằng feedback của phiên khác đã được tải vào môi trường hiện tại.
2. Phân tích ảnh/video nguồn; nhận diện chủ thể và bằng chứng có sẵn.
3. Tạo **3-5 ảnh độc lập** (4 mặc định), không chữ, 16:9. Đổi đồng thời câu chuyện/hành động + bố cục, không làm collage.
4. QA từng ảnh; trả ảnh thật, không chỉ prompt. Nếu công cụ thiếu khả năng làm đủ số ảnh, nói rõ số ảnh thực tế, không báo hoàn thành khống.
5. Ghi `run_id`, `concept`, `story`, `camera`, `scale_level` vào manifest.
6. Khi user **chọn hoặc nhận xét**, ghi event vào feedback journal. Ví dụ:
   - `cây vẫn hơi nhỏ` ⇒ `decision=revise`, `issue=too_small`, mức scale 3→đề xuất 4.
   - `cái thứ hai đẹp nhất` ⇒ `decision=selected`, `concept=B`.
   - `các ảnh giống nhau` ⇒ `decision=revise`, `issue=same_concept`.
   - `ảnh có chữ` ⇒ `decision=revise`, `issue=text_logo`.
   - `không có xe chở` ⇒ `decision=revise`, `issue=missing_truck`.
7. Tính đề xuất cho lần tạo tiếp theo bằng `scripts/feedback_loop.py recommend`. **Áp dụng các đề xuất mềm** và lưu lại quyết định. User vẫn có thể chỉnh scale 1-5 trực tiếp; yêu cầu hiện tại của user ưu tiên hơn đề xuất thống kê.
8. Nếu có video, kiểm tra cảnh khớp; nếu chưa có, ghi `SCENE_MATCH_PENDING`. Thu thập đánh giá của người dùng sau chỉnh sửa để khép vòng lặp.
9. **Lưu snapshot feedback** ngoài thư mục preview xóa sau 5h, hoặc xuất file feedback cho user tải về khi môi trường chỉ tồn tại tạm thời. Không coi bản lưu trong phiên sandbox tạm là lưu lâu dài trên Claude Chat.

## Phạm vi tự động hóa

- Có thể **tự ghi nhận và cải thiện ở các lần tương tác kế tiếp** khi agent có quyền chạy Python và có nơi lưu feedback bền vững (ví dụ workspace/project cục bộ).
- Không tự chạy 24/7, không huấn luyện lại mô hình, không truy cập dữ liệu kênh/CTR trừ khi người dùng cung cấp hoặc kết nối có quyền rõ ràng.
- Không thay đổi các quy tắc chống spam/chính sách YouTube để tối ưu hiệu suất. Không dùng chỉ số CTR như bảo đảm đạt chính sách.
- Không xóa ảnh ChatGPT/CDN hoặc ngăn người khác sao chép ảnh đã xem. Chỉ vault preview cục bộ có cleanup 5h như v2.2.
