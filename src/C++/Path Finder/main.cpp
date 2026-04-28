#include <iostream>
#include <vector>
#include <queue>
using namespace std;

int main() {
    vector<string> grid = {
        "S..#",
        ".#..",
        "...E"
    };

    int n = grid.size();
    int m = grid[0].size();

    pair<int,int> parent[100][100];
    bool visited[100][100] = {false};

    int sx, sy, ex, ey;

    // find S and E
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (grid[i][j] == 'S') {
                sx = i; sy = j;
            }
            if (grid[i][j] == 'E') {
                ex = i; ey = j;
            }
        }
    }

    queue<pair<int,int>> q;
    q.push({sx, sy});
    visited[sx][sy] = true;

    int dx[4] = {1, -1, 0, 0};
    int dy[4] = {0, 0, 1, -1};

    bool found = false;

    while (!q.empty()) {
        auto [x, y] = q.front();
        q.pop();

        if (x == ex && y == ey) {
            found = true;
            break;
        }

        for (int d = 0; d < 4; d++) {
            int nx = x + dx[d];
            int ny = y + dy[d];

            if (nx >= 0 && ny >= 0 && nx < n && ny < m) {
                if (!visited[nx][ny] && grid[nx][ny] != '#') {
                    visited[nx][ny] = true;
                    parent[nx][ny] = {x, y};
                    q.push({nx, ny});
                }
            }
        }
    }

    if (!found) {
        cout << "No path found\n";
        return 0;
    }

    // 🔥 backtrack path
    int x = ex, y = ey;

    while (!(x == sx && y == sy)) {
        if (grid[x][y] != 'E')
            grid[x][y] = '*';

        auto p = parent[x][y];
        x = p.first;
        y = p.second;
    }

    // print grid
    for (auto &row : grid)
        cout << row << "\n";

    return 0;
}