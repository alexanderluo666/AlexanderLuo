import java.awt.*;
import java.awt.event.*;
import java.util.PriorityQueue;
import javax.swing.*;

public class Main extends JPanel implements KeyListener, MouseListener {

    // ===== GRID =====
    static int n = 10;
    static int m = 10;

    static int cellSize = 50;

    static int[][] grid = new int[n][m]; 
    // 0 = empty, 1 = wall, 3 = path

    // ===== PLAYER =====
    int px = 0, py = 0;

    // ===== GOAL =====
    int gx = n - 1, gy = m - 1;

    // ===== AI =====
    boolean useAStar = true;
    boolean aiDone = false;

    boolean[][] visited = new boolean[n][m];
    int[][] parentX = new int[n][m];
    int[][] parentY = new int[n][m];
    int[][] dist = new int[n][m];

    static class Node {
        int x, y, g, f;
        Node(int x, int y, int g, int f) {
            this.x = x;
            this.y = y;
            this.g = g;
            this.f = f;
        }
    }

    PriorityQueue<Node> pq;

    // ===== UI =====
    javax.swing.Timer timer;
    JSlider speedSlider;
    JSlider scaleSlider;
    JButton modeBtn;
    JButton clearBtn;

    public Main() {

        setLayout(null);

        initAI();

        // ===== SPEED SLIDER =====
        speedSlider = new JSlider(50, 800, 200);
        speedSlider.setBounds(10, 520, 200, 40);

        speedSlider.addChangeListener(e -> {
            timer.setDelay(speedSlider.getValue());
        });

        // ===== SCALE SLIDER =====
        scaleSlider = new JSlider(30, 80, 50);
        scaleSlider.setBounds(220, 520, 200, 40);

        scaleSlider.addChangeListener(e -> {
            cellSize = scaleSlider.getValue();
            repaint();
        });

        // ===== MODE TOGGLE =====
        modeBtn = new JButton("A* Mode");
        modeBtn.setBounds(10, 570, 120, 40);

        modeBtn.addActionListener(e -> {
            useAStar = !useAStar;
            modeBtn.setText(useAStar ? "A* Mode" : "Dijkstra Mode");
            initAI();
        });

        // ===== CLEAR PATH =====
        clearBtn = new JButton("Clear Path");
        clearBtn.setBounds(140, 570, 120, 40);

        clearBtn.addActionListener(e -> clearPath());

        add(speedSlider);
        add(scaleSlider);
        add(modeBtn);
        add(clearBtn);

        addKeyListener(this);
        addMouseListener(this);
        setFocusable(true);

        // ===== FIXED TIMER (NO AMBIGUITY) =====
        timer = new javax.swing.Timer(200, e -> stepAI());
        timer.start();
    }

    // ================= AI INIT =================
    void initAI() {

        pq = new PriorityQueue<>((a, b) -> a.f - b.f);
        aiDone = false;

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                visited[i][j] = false;
                parentX[i][j] = -1;
                parentY[i][j] = -1;
                dist[i][j] = Integer.MAX_VALUE;
            }
        }

        dist[0][0] = 0;
        pq.add(new Node(0, 0, 0, heuristic(0, 0)));
    }

    // ===== HEURISTIC (A*) =====
    int heuristic(int x, int y) {
        return Math.abs(x - gx) + Math.abs(y - gy);
    }

    // ================= AI STEP =================
    void stepAI() {
        if (pq.isEmpty() || aiDone) return;

        Node cur = pq.poll();
        int x = cur.x, y = cur.y;

        if (visited[x][y]) return;
        visited[x][y] = true;

        if (x == gx && y == gy) {
            aiDone = true;
            drawPath();
            repaint();
            return;
        }

        int[] dx = {1, -1, 0, 0};
        int[] dy = {0, 0, 1, -1};

        for (int d = 0; d < 4; d++) {

            int nx = x + dx[d];
            int ny = y + dy[d];

            if (nx < 0 || ny < 0 || nx >= n || ny >= m) continue;
            if (grid[nx][ny] == 1) continue;

            int newG = cur.g + 1;

            if (newG < dist[nx][ny]) {
                dist[nx][ny] = newG;

                int f = useAStar ? newG + heuristic(nx, ny) : newG;

                pq.add(new Node(nx, ny, newG, f));

                parentX[nx][ny] = x;
                parentY[nx][ny] = y;
            }
        }

        repaint();
    }

    // ===== DRAW PATH =====
    void drawPath() {
        int x = gx, y = gy;

        while (!(x == 0 && y == 0)) {
            grid[x][y] = 3;

            int px = parentX[x][y];
            int py = parentY[x][y];

            x = px;
            y = py;
        }
    }

    // ===== CLEAR PATH =====
    void clearPath() {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (grid[i][j] == 3) grid[i][j] = 0;
            }
        }
        repaint();
    }

    // ================= PLAYER MOVEMENT =================
    public void keyPressed(KeyEvent e) {

        int nx = px, ny = py;

        if (e.getKeyCode() == KeyEvent.VK_W || e.getKeyCode() == KeyEvent.VK_UP) nx--;
        if (e.getKeyCode() == KeyEvent.VK_S || e.getKeyCode() == KeyEvent.VK_DOWN) nx++;
        if (e.getKeyCode() == KeyEvent.VK_A || e.getKeyCode() == KeyEvent.VK_LEFT) ny--;
        if (e.getKeyCode() == KeyEvent.VK_D || e.getKeyCode() == KeyEvent.VK_RIGHT) ny++;

        if (nx >= 0 && ny >= 0 && nx < n && ny < m && grid[nx][ny] != 1) {
            px = nx;
            py = ny;
        }

        if (px == gx && py == gy) {
            System.out.println("🎉 YOU WIN!");
        }

        repaint();
    }

    public void keyReleased(KeyEvent e) {}
    public void keyTyped(KeyEvent e) {}

    // ================= MAZE EDIT =================
    public void mousePressed(MouseEvent e) {

        int y = e.getX() / cellSize;
        int x = e.getY() / cellSize;

        if (x >= 0 && y >= 0 && x < n && y < m) {

            if ((x == px && y == py) || (x == gx && y == gy)) return;

            grid[x][y] = (grid[x][y] == 1) ? 0 : 1;

            repaint();
        }
    }

    public void mouseReleased(MouseEvent e) {}
    public void mouseClicked(MouseEvent e) {}
    public void mouseEntered(MouseEvent e) {}
    public void mouseExited(MouseEvent e) {}

    // ================= DRAW =================
    public void paintComponent(Graphics g) {
        super.paintComponent(g);

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {

                if (i == px && j == py) g.setColor(Color.BLUE);
                else if (i == gx && j == gy) g.setColor(Color.RED);
                else if (grid[i][j] == 1) g.setColor(Color.BLACK);
                else if (grid[i][j] == 3) g.setColor(Color.YELLOW);
                else if (visited[i][j]) g.setColor(Color.CYAN);
                else g.setColor(Color.WHITE);

                g.fillRect(j * cellSize, i * cellSize, cellSize, cellSize);
                g.setColor(Color.GRAY);
                g.drawRect(j * cellSize, i * cellSize, cellSize, cellSize);
            }
        }
    }

    // ================= MAIN =================
    public static void main(String[] args) {

        JFrame frame = new JFrame("AI Maze Game");

        Main game = new Main();

        frame.add(game);
        frame.setSize(600, 650);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);

        game.requestFocusInWindow();
    }
}