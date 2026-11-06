---
name: thumbnail-first-scene-match
version: 2.3.0
description: Dùng khi người dùng yêu cầu thiết kế, tạo, chỉnh hoặc đánh giá thumbnail YouTube từ ảnh/video gốc cây khổng lồ; đặc biệt xe thực sự chở thân cây, phóng to cây, scale 1-5, 3-5 phương án 16:9 không chữ, scene match. Auto-recognize thumbnail/ảnh bìa/xe chở gốc cây, và ghi feedback lựa chọn/sửa ảnh để cải tiến lần sau. Không kích hoạt nếu chỉ hỏi về ảnh không liên quan tới thumbnail.
---
# THUMBNAIL FIRST > SCENE MATCH | SKILL v2.3: AUTO-RECOGNITION + FEEDBACK LOOP + SCALE

**ĐỌC TRƯỚC KHI TẠO:** `profile/AUTO_RECOGNITION_AND_FEEDBACK.md`, `profile/SESSION_CREATIVE_BRIEF.md`, `profile/creative_profile.json` và `templates/NO_TEXT_BATCH_PROMPTS.md`. Đây là các ràng buộc sáng tạo được rút từ chuỗi yêu cầu và lần chỉnh sửa trong cùng phiên làm việc, không phải ví dụ quảng cáo. `config/defaults.json` là cài đặt mặc định.

## 0A. Tự nhận diện yêu cầu (sau khi Skill được cài / bật)

Claude hoặc một agent hỗ trợ Skills **chỉ có thể tự chọn dùng Skill sau khi đã được cài/enable**. Khi user tải ảnh/video lên và nói “làm thumbnail”, “cho xe chở gốc cây”, “cây to hơn”, “tạo 3-5 ảnh bìa”, hãy nhận diện nhiệm vụ và nạp Skill; không bắt user phải gõ đúng tên. Khi user chỉ đưa đánh giá/chọn ảnh, kích hoạt **feedback recording** thay vì mặc định tạo lại 4 ảnh. Quy tắc đầy đủ trong `profile/AUTO_RECOGNITION_AND_FEEDBACK.md`. **Chỉ đính kèm ZIP vào chat chưa phải cài Skill.**

## 0. NHIỆM VỤ MẶC ĐỊNH, KHÔNG ĐƯỢC LÀM SAI

Người dùng sản xuất thumbnail chủ yếu cho **khán giả quốc tế**. **TẤT CẢ THUMBNAIL MẶC ĐỊNH KHÔNG CÓ BẤT KỲ TEXT NÀO**: không tiếng Việt, không tiếng Anh, không chữ/số nhỏ, thông số tuổi/kích thước, mũi tên, biểu tượng chữ, logo, watermark, nhãn dán, biển hiệu đọc được hoặc chú thích trên đầu cây/xe. Dùng **hình ảnh thuần túy** để gây tò mò. Không tạo poster/infographic/collage thay cho thumbnail. Các mã A/B/C/D chỉ dùng làm **tên file/caption bên ngoài ảnh**. Chỉ thay đổi quy tắc không chữ nếu người dùng **chủ động yêu cầu cụ thể** ở một lượt tương lai.

Một lần chạy phải trả **3-5 ẢNH RIÊNG 16:9**, mặc định **4 ẢNH**. Nếu công cụ hỗ trợ sinh đồng thời n=4, dùng batch; nếu không, thực hiện 4 lần tạo riêng có prompt cố ý khác nhau. Không thay 4 ảnh bằng 4 lời mô tả, prompt, storyboard hoặc bảng 4 ô. Không giả vờ đã tạo ảnh/video nếu chưa có đầu ra thật.

Với các ảnh tham chiếu gốc cây hiện tại: **HÌNH ẢNH BẮT BUỘC LÀ XE ĐANG CHỞ GỐC CÂY CỰC KỲ KHỔNG LỒ**. Khúc gỗ phải đặt và được giữ thực sự trên thùng trailer đa trục nối với đầu kéo nhìn thấy được. Không được trả hình chỉ có gỗ, chỉ slab, chỉ cẩu treo, hoặc cảnh một chiếc xe ở xa không trực tiếp chở nó. Đây là yêu cầu người dùng đã nhấn mạnh lặp lại nhiều lần.

## 1. Creative DNA: yêu cầu người dùng trong phiên

### A. Chủ thể & độ phóng đại
- Giữ đặc điểm nhận dạng của **đúng khúc gỗ** từ ảnh nguồn: mặt cắt méo không đều, nứt/rạn thật, vỏ thô sẫm, các mảng nâu xám, vết lồi lõm, thân thuôn. Tránh tự thay gốc cây thành vật liệu mới, slab bóng, hoặc mặt gỗ vân neon nhiều màu.
- **Tham số scale có thể chỉnh ở các lượt sau**: nếu người dùng yêu cầu “to hơn”, “cực kỳ khổng lồ hơn nữa”, “scale level 4/5”, hãy tăng **mức phóng đại kích thước** mà vẫn giữ nguyên nhận diện khúc gỗ và logic xe chở. Dùng phối cảnh, góc máy, tương quan với cabin/bánh xe/công nhân và chiều dài trailer để tăng cảm giác khổng lồ; không thêm số đo giả và không làm kết cấu log biến dạng phi lý.
- Ưu tiên cảm giác **cực kỳ khổng lồ** thông qua góc thấp, perspective và đối chiếu công nhân nhỏ/cabin/bánh xe/xưởng; đừng bịa các con số để gây sốc.
- Trọng tâm là quy mô và sức nặng, nhưng gốc cây vẫn phải có hình dáng, chi tiết bề mặt đáng tin như tư liệu công nghiệp.

### B. Vận tải là hành động chính
- Có **đầu kéo + trailer siêu trường nhiều trục + khúc gỗ thực sự đặt lên trailer + kê/chằng/neo** rõ ràng.
- Gốc cây không lơ lửng trên cẩu trong phiên bản tuyên bố “xe chở”; cảnh bốc dỡ chỉ hợp lệ khi gốc gỗ đã được đặt vững trên xe (cẩu có thể ở hậu cảnh hoặc cáp chùng).
- Chọn khung hình sao cho khán giả chỉ nhìn 1 giây đã thấy xe đang vận chuyển khúc gỗ, không phải hiểu thông qua caption.

### C. Ngôn ngữ thị giác
- 16:9, photorealism / cinematic industrial documentary, góc máy mạnh, bầu trời và xưởng gỗ tự nhiên, vật liệu sắc nét; ánh sáng đẹp nhưng không CGI giả tạo.
- Công nhân nhỏ hoặc vật chuẩn kích thước là phụ trợ, không lấn chủ thể. **Không văn bản, thông số, tên kênh, bảng quy trình hoặc watermark trên ảnh**.
- Ảnh cho khán giả nước ngoài **không cần chuyển sang tiếng Anh**: text-free mới là mặc định.

### D. Bài học từ những lần thử trước
- Ảnh không có xe: FAIL bất kể gỗ đẹp. Ảnh có xe nhưng gốc cây đang treo lơ lửng: FAIL nếu lời hứa là vận tải.
- Ảnh có chữ giả như số đo, tên thương hiệu, ký hiệu lên gỗ: FAIL. Nếu công cụ tự thêm text: tái tạo/xóa text trước khi giao.
- Một collage giới thiệu Skill có nhiều ô và tiêu đề KHÔNG PHẢI bộ 4 thumbnail đầu ra. Phải giao file A/B/C/D độc lập.
- Bốn ảnh đều là rơ-moóc đỏ/gốc cây lấp khung cùng góc nhìn, chỉ thay crop: **không đủ độc bản**. Buộc thay action/story + camera.

## 2. Batch 3-5 concept có sự khác biệt thực chất

| ID | Câu chuyện trong 1 giây | Cách quay chính | Điểm khác biệt bắt buộc |
|---|---|---|---|
| A | Kích cỡ mặt cắt khúc gỗ khi xe đang mang tải | cận thấp từ đuôi 3/4 | mặt gỗ tiền cảnh, trailer và cabin chạy sâu |
| B | Đoàn xe khổng lồ tiến vào khu xưởng | cao/toàn cảnh 3/4 | thấy **toàn bộ đoàn xe**, nhà xưởng và người điều phối |
| C | Thử thách kỹ thuật vận chuyển siêu trường | góc thấp ngang hông | dãy trục, giá kê, dây chằng, khúc gỗ ở góc ngang |
| D | Đầu kéo xoay vào cổng với khối gỗ phía sau | trước 3/4 chéo | cabin rõ ở tiền cảnh, thấy gốc gỗ thật sự trên trailer |
| E | Chuẩn bị dỡ hàng khi xe đã dừng (tùy chọn) | rộng ở điểm dỡ | xe/gỗ vẫn tiếp xúc; móc cẩu chưa nâng khúc gỗ |

Mỗi concept phải có ít nhất **3 khác biệt thực chất** so với các concept còn lại, trong đó tối thiểu (1) khác **ACTION/STORY** và (2) khác **CAMERA/COMPOSITION**. Đừng phụ thuộc vào đổi màu xe, filter, zoom/crop. Chọn câu chuyện dựa trên video/cảnh quay hoặc dựng cảnh được người dùng cho phép; không tưởng tượng thành một sự kiện thật nếu không có nguồn.

Các bộ sản phẩm gỗ khác (xẻ/cắt CNC/ván slab/nội thất) chỉ dùng khi người dùng đổi chủ đề video tương ứng; không chen vào batch có mục tiêu riêng là **xe chở gốc cây**.

## 2A. Tham số chỉnh kích thước (SIZE AMPLIFICATION)

Mặc định dùng `size_amplification.default_level = 3`. Khi người dùng yêu cầu cây gỗ **to hơn**, agent phải cho phép chỉnh tham số thay vì coi đó là yêu cầu ngoài skill.

- **Level 1**: gần kích thước tham chiếu, nhấn mạnh tính thực.
- **Level 2**: to hơn nhẹ nhưng vẫn thiên về realism.
- **Level 3**: rất to, đủ mạnh cho thumbnail, mặc định.
- **Level 4**: siêu khổng lồ, tạo wow-factor rõ rệt.
- **Level 5**: cực đại, chỉ dùng khi người dùng nhấn mạnh “khổng lồ hơn nữa”; vẫn phải giữ xe chở hợp lý.

**Quy tắc áp dụng:**
1. Ưu tiên tăng cảm nhận quy mô bằng góc máy thấp, lens wide hợp lý, đối tượng so sánh nhỏ và trailer dài hơn.
2. Không biến gốc cây thành một hình dạng mới.
3. Không thêm text đo đạc/tuổi cây để “chứng minh” kích thước.
4. Nếu scale tăng, QC phải kiểm tra lại: xe còn đang thực sự chở được log? bố cục còn đáng tin?
5. Khi người dùng nói “to hơn”, có thể sửa chính concept cũ thay vì phải đổi toàn bộ câu chuyện.

## 3. Quy trình bắt buộc: THUMBNAIL FIRST > VIDEO SCENE MATCH

1. Đọc creative profile và yêu cầu hiện tại. Phân tích ảnh nguồn, video và footage được phép dùng, rồi lập `Evidence Ledger` (`real_verified` / `ai_reconstruction` / `unsupported`). Nếu chỉ có ảnh gốc cây trong xưởng, toàn bộ cảnh xe vận chuyển là **AI reconstruction**, không được tự gọi là footage quay thật.
2. Chọn 3-5 ý tưởng phù hợp, có hành động khác nhau; chuẩn bị negative prompt **NO TEXT** cho từng ảnh.
3. Tạo **3-5 ảnh thumbnail riêng** với công cụ ảnh, 16:9, không chữ. Xuất từng ảnh độc lập, filenames A/B/C/D(/E). Nếu có một ảnh sai thì sửa chính ảnh đó trước khi giao, không thay bằng poster tổng hợp.
4. Visual QA **từng ảnh**: đúng thân cây? cây rất khổng lồ? XE THỰC SỰ CHỞ? có cabin/trailer nhiều trục? 16:9? không chữ/số/logo/watermark? không hình học lạ? Nếu một mục MUST trượt: **REVISE**.
5. Novelty QA: so sánh giữa tất cả ảnh trong batch, 20 thumbnail gần đây của kênh nếu người dùng cung cấp và thumbnail thị trường có bằng chứng nếu khả dụng. Nếu lặp motíf: dựng lại concept khác, không dùng đổi crop/màu như một sửa chữa đủ.
6. Giao ngay 3-5 ảnh, mô tả các khác biệt **trong lời nhắn, không trên ảnh**. Người dùng chọn một ảnh hoặc yêu cầu chỉnh.
7. Sau khi chốt thumbnail, gán `selected_thumbnail_id` ↔ `scene_match_id`. Thiết kế một **cảnh video tương ứng về chủ thể, xe, góc nhìn/hành động** đủ để khán giả nhận ra. Gắn source/timecode/duration/provenance cho cảnh; có thể gồm establishing > cảnh gần như thumbnail > close-up thật/cảnh tiếp nối > quy trình xưởng. Không chèn duy nhất một still giả tạo vào footage không liên quan chỉ để hợp thức hóa.
8. Khi dựng thực tế, phải có **video, công cụ edit và bằng chứng timecode** rồi mới đánh dấu `SCENE_MATCH_PASS`. Nếu chỉ có ảnh: `SCENE_MATCH_PENDING`; lập plan, không khẳng định đã chèn MP4.
9. Kiểm tra metadata không gây hiểu lầm; giá trị sáng tạo toàn video (narrative/biên tập/thuyết minh), nguồn footage/music, quyền sử dụng, và quyết định altered/synthetic disclosure trên YouTube Studio khi áp dụng. Không bảo đảm chắc chắn tránh khiếu nại/YPP/spam chỉ bằng thumbnail.
10. Lưu bản preview vào vault cục bộ TTL 5 giờ (nếu môi trường cho phép), cho phép lưu bản xuất đã duyệt vào kho riêng; xuất báo cáo `PASS/REVISE/BLOCK` đầy đủ.

## 4. Negative prompt không chữ: ALWAYS ON

**Apply to every image generation call:** “No text anywhere in the image, no letters, no words, no numerals, no dimensions, no wood markings, no annotations, no arrow graphics, no captions, no stickers, no watermark, no channel logo, no branding, no readable license plates or signboards, no title design, no tutorial layouts, no infographic, no contact sheet, no split panel, no fake technical callout. Photorealistic single full-bleed 16:9 frame only.”

**Grounded transport:** “Exactly the recognizably same rough monumental trunk as the reference is actually supported on the heavy-duty connected multi-axle truck/trailer, with plausible cradles and safety restraints; never hovering in slings, never resting on the ground next to an unrelated truck.”

Tham khảo các prompt camera-specific trong `templates/NO_TEXT_BATCH_PROMPTS.md`. Không cho công cụ vẽ label A/B/C/D trong ảnh.

## 5. Lưu trữ/xóa tự động preview sau 5 giờ

- `scripts/preview_vault.py register`: tạo **bản sao được quản lý cục bộ**, lưu `created_utc`, `expires_utc = created + 5h` theo cấu hình.
- `scripts/install_windows_cleanup.ps1`: đăng ký Windows Task Scheduler chạy cleanup **5 phút/lần**. Nếu máy tắt, việc xóa không thể xảy ra đúng giờ, sẽ thực hiện ở lần chạy tiếp theo.
- **CHỈ xóa bản preview nằm trong vault do người dùng cài.** Không xóa ảnh nguồn, bản xuất cuối đã duyệt, scene assets trong video, ảnh trong ChatGPT/CDN hay bản sao đã tới thiết bị khác. Không tuyên bố có quyền xóa remote assets hoặc bảo vệ 100% khỏi chụp màn hình/tải xuống.
- Khuyến nghị preview vault private và không chia sẻ URL công khai. Nếu cần giữ ảnh sau 5h để hoàn thiện video, xuất bản được duyệt sang đường dẫn riêng trước khi hết hạn.
- Có test an toàn ở `tests/test_preview_vault.py`.

## 6. Chính sách YouTube & trung thực nội dung

- **Thumbnail truthful:** Không hứa có xe chở một khúc gỗ mà video không có một phân đoạn tương ứng; không biến một ảnh AI tái dựng thành chứng cứ quay thật.
- **Reused & inauthentic:** 4 thumbnails khác nhau không tự chứng minh mỗi video độc bản; cần nội dung biên tập/thuyết minh/footage có đóng góp rõ. Không vận hành dây chuyền cùng công thức lặp chỉ đổi một vài thứ nhỏ.
- **Disclosure:** Đánh giá yêu cầu khai báo altered/synthetic content khi đưa cảnh AI chân thực vào video; không tự động kết luận trường hợp nào cũng miễn khai báo hoặc bắt buộc khai báo.
- **Titles:** Thumbnail KHÔNG CHỮ, còn tiêu đề/description nằm ở **metadata YouTube bên ngoài ảnh**. Đa dạng cấu trúc và đúng nội dung, không bịa tuổi cây/độ dài/tải trọng.
- Không đề nghị xóa/ẩn hàng loạt video đang kháng cáo chỉ để làm sạch kênh. Preview cleanup không tác động đến YouTube upload.

Nguồn chính thức để kiểm tra tại thời điểm vận hành:
- https://support.google.com/youtube/answer/1311392
- https://support.google.com/youtube/answer/2801973
- https://support.google.com/youtube/answer/14328491
- https://developers.google.com/youtube/terms/revision-history

## 7. Kết quả cần trả

- `thumbnails/A.png`, `B.png`, `C.png`, `D.png` (và `E.png` nếu chọn 5), **mỗi ảnh riêng, không text, 16:9**.
- `manifest.json`: source/provenance, concept storyboard/camera, scene_match_id, thời điểm tạo/hết hạn preview managed, các trạng thái.
- `scene_match_plan.md`: cảnh đúng gốc cây/xe, nguồn real hay AI, timecode nếu có, QC cảnh tương ứng.
- `originality_qc.md`: no-text visual review cho từng ảnh, câu chuyện khác biệt, quyền nguồn, rủi ro reused/inauthentic/AI.
- Báo cáo tóm tắt concept A-D bằng text **bên ngoài ảnh**, ghi rõ `SCENE_MATCH_PENDING` khi chưa dựng video.

**Quality Gate cuối cùng:** Nếu chỉ tạo ra một infographic quảng bá Skill, chỉ prompt, một collage, một ảnh có bất cứ chữ/số nào, hoặc một gốc cây không thật sự nằm trên xe chở > nhiệm vụ **CHƯA HOÀN THÀNH**.

## 7. FEEDBACK LOOP: cải tiến mỗi lượt, không cần lặp lỗi cũ

**Vòng bắt buộc:** Generate 3-5 independent concepts > Visual/novelty/scene QA > Deliver > Collect user's choice/corrections > Record feedback > Recommend safe changes > Apply to NEXT batch > Compare results.

- Ghi nhận `run_id`, ảnh A/B/C/D(/E), camera, story, scale level, quyết định của user (`selected/revise/rejected/published`), lỗi cụ thể và đánh giá (nếu có). **Không tự bịa feedback, CTR hoặc số liệu kênh.**
- Công cụ: `python scripts/feedback_loop.py record --run-id ... --concept ... --decision ... --issue ...` và `python scripts/feedback_loop.py recommend --current-scale 3`. Hướng dẫn `docs_INSTALL.md`.
- Nếu user nói **“cây còn nhỏ / to thêm nữa”** ⇒ ghi `too_small`, đề xuất tăng 1 level (tối đa 5); nếu user chỉ định scale cụ thể thì dùng scale đó. Nếu user nói **“trùng ý tưởng”** ⇒ thay **câu chuyện + góc máy**, không chỉ đổi xe màu khác. Nếu **“xe không chở cây”**, **“có chữ/logo”** ⇒ ảnh bị fail/REVISE và ghi lỗi. Nếu user chọn B ⇒ ghi `selected=B` và dùng nhận xét để hiểu sở thích mềm, **không tự động lặp B cho các video sau**.
- Đọc báo cáo feedback trước khi lên concept mới; ghi giải thích ngắn điều gì đã thay đổi. **Không ghi đè quy tắc cứng** về no-text/16:9/truck support/độc bản/trung thực với video/chính sách.
- Lưu feedback JSON ngoài vault preview 5h: `~/.thumbnail_first_scene_match/feedback/feedback.json` hoặc `THUMBNAIL_FEEDBACK_FILE`. Nếu môi trường chat không có lưu bền vững, xuất file JSON để user lưu/tải lại cho phiên sau. Không tự hứa “học liên tục 24/7” hoặc tự huấn luyện model. Không sử dụng feedback để khẳng định video đã qua YouTube review.
- Kiểm thử: `python tests/test_feedback_loop.py`.
