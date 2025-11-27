# 版本遷移工具

此目錄包含版本遷移相關的工具和腳本。

## 支援的遷移路徑

- v1 → v2: Python 無人機 → 多語言島嶼
- v2 → v1: 多語言島嶼 → Python 無人機 (降級)

## 使用方式

### 透過 automation-entry.sh

```bash
./automation-entry.sh
# 選擇選項 5: 版本遷移
```

### 直接執行遷移腳本

```bash
# v1 → v2 遷移
bash migration/v1-to-v2.sh

# v2 → v1 遷移 (降級)
bash migration/v2-to-v1.sh
```

## 注意事項

- 遷移前會自動建立備份
- 請確保所有變更已提交至版本控制
- 生產環境遷移前請先在測試環境驗證
