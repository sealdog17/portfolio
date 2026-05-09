from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

API_KEY = "7CEB464E0571FA7E45AB6BCB45791827"
STEAM_ID = "76561199381120716"


@app.route("/games")
def get_games():
    url = (
        f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
        f"?key={API_KEY}&steamid={STEAM_ID}&include_appinfo=1&include_played_free_games=1"
    )
    try:
        response = requests.get(url)
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"})


@app.route("/hobby-games")
def get_hobby_games():
    """Trả về danh sách game kèm URL ảnh header để hiển thị trong trang Hobby"""
    url = (
        f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
        f"?key={API_KEY}&steamid={STEAM_ID}&include_appinfo=1&include_played_free_games=1"
    )
    try:
        response = requests.get(url)
        data = response.json()
        games_raw = data.get("response", {}).get("games", [])

        # Sắp xếp theo thời gian chơi nhiều nhất, lấy tối đa 12 game
        games_sorted = sorted(games_raw, key=lambda g: g.get("playtime_forever", 0), reverse=True)

        games = []
        for g in games_sorted[:12]:
            appid = g.get("appid")
            games.append({
                "appid": appid,
                "name": g.get("name", "Unknown"),
                "playtime_hours": round(g.get("playtime_forever", 0) / 60, 1),
                # Ảnh header game (460x215)
                "header_image": f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg",
                # Ảnh capsule nhỏ (231x87)
                "capsule_image": f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/capsule_231x87.jpg",
                # Link mở trang Store của game
                "store_url": f"https://store.steampowered.com/app/{appid}",
            })

        return jsonify({"games": games, "total": len(games_raw)})

    except Exception as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"})


@app.route('/')
def Home():
    return render_template('Main_dashboard.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
