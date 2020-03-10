#include<bits/stdc++.h>
using namespace std;
int n, m;
vector<string> mass;
vector<vector<int> > cl;
set<pair<int, int> > points;
vector<pair<int, int> > s;
void dfs(int i, int j, int ib, int jb)
{
    s.push_back(make_pair(i, j));
    cl[i][j] = 1;
    for(int dx = -1; dx <= 1; dx++)
    {
        for(int dy = -1; dy <= 1; dy++)
        {
            if(abs(dx) + abs(dy) != 1)
            {
                continue;
            }
            int x = i + dx;
            int y = j + dy;
            if(x >= 0 && y >= 0 && x < n && y < m && mass[x][y] == '.' && (x != ib || y != jb) && cl[x][y] != 2)
            {
                if(cl[x][y] == 1)
                {
                    int now = s.size() - 1;
                    while(s[now] != make_pair(x, y))
                    {
                        points.insert(s[now]);
                        now--;
                    }
                    points.insert(s[now]);
                    continue;
                }
                dfs(x, y, i, j);
            }
        }
    }
    cl[i][j] = 2;
    s.pop_back();
}

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
    cin >> n >> m;
    mass.resize(n);
    cl.resize(n);
    for(int i = 0; i < n; i++)
    {
        cin >> mass[i];
        cl[i] = vector<int>(m, 0);
    }
    for(int i = 0; i < n; i++)
    {
        for(int j = 0; j < m; j++)
        {
            if(mass[i][j] == '.' && cl[i][j] == 0)
            {
                s.clear();
                dfs(i, j, -1, -1);
            }
        }
    }
    for(int i = 0; i < n; i++)
    {
        for(int j = 0; j < m; j++)
        {
            if(mass[i][j] == '.')
            {
                mass[i][j] = 'X';
            }
        }
    }
    auto it = points.begin();
    for(; it != points.end(); it++)
    {
        mass[it->first][it->second] = '.';
    }
    for(int i = 0; i < n; i++)
    {
        cout << mass[i] << endl;
    }
}
