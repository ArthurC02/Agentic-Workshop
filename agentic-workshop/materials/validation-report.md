# Materials 修正驗證報告

> 讀者：主持人與維護者。時機：發放前。前置：[操作說明](README.md)。可見性：內部，不發學員。

本輪已修正 Time Skip 解鎖頁為29分鐘；60秒例外倒數支援開始／暫停／繼續／重設，講者控制同一倒數，B3段落計時持續。

單檔Runbook內嵌G0／B0及兩份受控Recovery；Recovery只於52／63分鐘由主持人視需要提供獨立碼，一般B2／B3碼不開Recovery。切換頁包含保存成果、新目錄、停Server、Python3.13環境、44／55測試、Health及新Session／Context紀錄；不以接續基線當小組完成，不發B3解答。

安全交付包由`python -X utf8 scripts/package_materials.py`產生於`dist/materials/participant-materials.zip`，精確只含`runbook.html`。不要自行打包原稿資料夾。

實測：134項教材／打包測試通過；兩份HTML重建一致；三份JS語法檢查通過，倒數純狀態驗證通過；四份嵌入ZIP與凍結候選字節及SHA256相同，下載檔名符合操作指令。證據見[驗證JSON](validation-evidence.json)。凍結候選及應用程式未修改，未重跑應用套件。

完成條件：上述技術檢查通過，學員只收成品HTML或安全ZIP。目標瀏覽器的離線解鎖、下載政策、表單、講者視窗與版面仍須Preflight實測；真人90分鐘與正式發布未執行，本輪技術通過不代替現場驗收。
