# Lab 7

- `local-test.log` được tạo khi chạy `python -m unittest discover -s tests -v`.
- Sau khi GitHub Actions chạy thành công, tải raw log về
  `github-actions-run.log`.
- Sau khi các commit được tạo, xuất `git log` vào `git-history.log`.

Hai log sau phụ thuộc vào thao tác commit/push trên GitHub nên không được tạo
khống khi chưa có lần chạy CI thành công.
