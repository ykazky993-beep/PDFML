from pathlib import Path
from pdfml.lexer import Lexer, LexerError
from pdfml.parser import Parser, ParserError
from pdfml.compiler import PDFMLCompiler
import argparse

def print_help():
    print("""
=== BANTUAN SINTAKS PDFML v3 ===
Sintaks menggunakan tanda kurung kurawal mirip HTML.

[TAG DASAR]
{head align="center" color="blue"}Judul Utama{/head}
{sub color="#FF0000"}Sub Judul{/sub}
{body}Ini adalah teks paragraf biasa.{/body}

[INLINE STYLE]
Di dalam {body}, Anda bisa menambahkan:
{b}Tebal{/b}, {i}Miring{/i}, {u}Garis Bawah{/u}
{color val="green"}Teks Hijau{/color}

[MEDIA & STRUKTUR]
{image src="foto.png" width=200 height=150 /}  <-- Catat: Self closing!
{space height=30 /}                            <-- Jarak kosong
{page /}                                       <-- Halaman baru

[TABEL]
{table border=1}
    {row}{cell}No{/cell}{cell}Nama{/cell}{/row}
    {row}{cell}1{/cell}{cell}Budi{/cell}{/row}
{/table}

[PERINTAH CLI]
help     : Bantuan sintaks
clear    : Hapus isi buffer saat ini
load     : Memuat sintaks dari file eksternal (contoh.pdfml)
compile  : Render PDF dan keluar
exit     : Keluar tanpa menyimpan
""")

def main():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("-c", "--compile", help="File PDFML")
    arg_parser.add_argument("-o", "--output", help="Output PDF")

    args = arg_parser.parse_args()   # <-- WAJIB ADA

    if args.compile:
        file_path = args.compile

        with open(file_path, "r", encoding="utf-8") as f:
            buffer = f.read()

        output = args.output or "output.pdf"

        lexer = Lexer(buffer)
        tokens = lexer.get_tokens()

        parser = Parser(tokens)
        ast_nodes = parser.parse()

        compiler = PDFMLCompiler(output)
        compiler.compile(ast_nodes)

        return
    print("=========================================")
    print("   PDFML v3 - Abstract Syntax Compiler   ")
    print("=========================================")
    filename = input("Masukkan nama file PDF output (misal: hasil.pdf): ").strip()
    if not filename.endswith(".pdf"):
        filename += ".pdf"

    state = "COMMAND"
    buffer = ""
    
    print("Ketik 'help' untuk panduan. Ketik 'compile' untuk mencetak PDF.")
    while True:
        try:
            # Prompt berdasarkan state
            prompt = "pdfml> " if state == "COMMAND" else "...  > "
            text = input(prompt)

# ==========================
# COMMAND MODE
# ==========================
            if state == "COMMAND":
                cmd = text.strip().lower()

                if not cmd:
                    continue

                if cmd == "help":
                    print_help()
                    continue

                elif cmd == "exit":
                    print("Dibatalkan.")
                    break

                elif cmd == "clear":
                    buffer = ""
                    print("[✓] Buffer dibersihkan.")
                    continue

                elif cmd == "load":
                    file_path = input("Masukkan lokasi file (.txt / .pdfml): ")
                    if Path(file_path).exists():
                        with open(file_path, "r", encoding="utf-8") as f:
                            buffer = f.read()
                            print(f"[✓] {len(buffer)} karakter termuat dari file.")
                    else:
                        print("[!] File tidak ditemukan.")
                        continue

                elif cmd == "edit":
                    state = "EDIT"
                    print("[*] Masuk mode edit. Ketik 'done' untuk selesai.")
                    continue

                elif cmd == "compile":
                    break

                else:
                    print("[!] Command tidak dikenal.")
                    continue

# ==========================
# EDIT MODE
# ==========================
            elif state == "EDIT":

                if text.strip().lower() == "done":
                    state = "COMMAND"
                    print("[✓] Keluar dari mode edit.")
                    continue

                buffer += text + "\n"

            # Cek apakah kurung kurawal sudah seimbang
            open_count = buffer.count('{')
            close_count = buffer.count('}')
            
            if open_count == close_count:
                # Semua tag tertutup (sementara dianggap block selesai)
                # Tunggu user ketik 'compile' atau tambah baris lagi.
                pass
                
        except KeyboardInterrupt:
            print("\nGunakan perintah 'exit' untuk membatalkan.")

    # --- PROSES KOMPILASI ---
    if not buffer.strip():
        print("[!] Dokumen kosong. Keluar.")
        return

    try:
        print("\n[*] 1. Menjalankan Lexer (Tokenizing)...")
        lexer = Lexer(buffer)
        tokens = lexer.get_tokens()

        print("[*] 2. Menjalankan Parser (Membangun AST)...")
        parser = Parser(tokens)
        ast_nodes = parser.parse()

        print("[*] 3. Menjalankan Compiler (Platypus Engine)...")
        compiler = PDFMLCompiler(filename)
        compiler.compile(ast_nodes)

    except LexerError as e:
        print(f"\n[ERROR - LEXER] {e}")
    except ParserError as e:
        print(f"\n[ERROR - PARSER] {e}")
    except Exception as e:
        print(f"\n[CRITICAL ERROR] {e}")

if __name__ == "__main__":
    main()

