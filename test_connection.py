import pyodbc

# Cấu hình kết nối
server = r'LAPTOP-8L0VDRJ8\KIET' # Hoặc IP SQL Server
database = 'HCSDL'
username = 'sa'
password = '123456'

try:
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};DATABASE={database};UID={username};PWD={password}'
    )
    print("Kết nối CSDL thành công!")
    conn.close()
except Exception as e:
    print("Không kết nối được tới CSDL.")
    print("Lỗi:", e)
