from utils import registered_players, players_scores, get_top_3_scores, reset_scores, reset_players

admin_password = "rm4u123"  # Password simple, boleh ubah

def admin_panel():
    print("=== RINGGIT FIGHTER ADMIN PANEL ===")
    password = input("Masukkan password admin: ")
    
    if password != admin_password:
        print("Password salah. Keluar.")
        return
    
    while True:
        print("\n1. Lihat semua pemain")
        print("2. Lihat Top 3 skor")
        print("3. Reset semua data")
        print("4. Keluar")
        
        pilihan = input("Pilih menu: ")
        
        if pilihan == "1":
            print("Senarai Peserta:")
            for player in registered_players:
                print("-", player)
        
        elif pilihan == "2":
            print("Top 3 Skor:")
            top_scores = get_top_3_scores()
            for score in top_scores:
                print("-", score)
        
        elif pilihan == "3":
            confirm = input("Betul nak reset semua? (ya/tidak): ")
            if confirm.lower() == "ya":
                reset_scores()
                reset_players()
                print("Data telah direset.")
        
        elif pilihan == "4":
            print("Keluar panel admin.")
            break
        
        else:
            print("Pilihan tidak sah. Cuba lagi.")

if __name__ == "__main__":
    admin_panel()
