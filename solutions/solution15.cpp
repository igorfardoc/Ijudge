#include<bits/stdc++.h>
using namespace std;
int mod = 1000000007;
int n, m, k;


using mat = array<array<int, 50>, 50>;
mat mul(mat a, mat b)
{
    mat c;
    for(int i = 0; i < n; i++)
    {
        c[i].fill(0);
        for(int j = 0; j < n; j++)
        {
            for(int k = 0; k < n; k++)
            {
                c[i][j] = (c[i][j] + (long long)a[i][k] * b[k][j]) % mod;
            }
        }
    }
    return c;
}
mat powmat(mat a, long long s)
{
    mat res;
    for(int i = 0; i < n; i++)
    {
        res[i].fill(0);
        res[i][i] = 1;
    }
    while(s)
    {
        if(s & 1)
        {
            res = mul(res, a);
        }
        a = mul(a, a);
        s >>= 1;
    }
    return res;
}
void print(mat a)
{
    for(int i = 0; i < n; i++)
    {
        for(int j = 0; j < n; j++)
        {
            cout << a[i][j] << " ";
        }
        cout << endl;
    }
}

int main()
{
    ios_base::sync_with_stdio(0);
    mat start;
    mat per;
    cin >> n >> m >> k;
    for(int i = 0; i < n; i++)
    {
        start[i].fill(0);
        per[i].fill(0);
    }
    for(int i = 0; i < m; i++)
    {
        int v, u;
        cin >> v >> u;
        v--;
        u--;
        per[v][u]++;
    }
    start[0][0] = 1;
    mat res = mul(start, powmat(per, k));
    int ans = 0;
    for(int i = 0; i < n; i++)
    {
        ans = (ans + res[0][i]) % mod;
    }
    cout << ans;
}
