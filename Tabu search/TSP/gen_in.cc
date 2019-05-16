#include<bits/stdc++.h>
using namespace std;

#define maxn 10000

double x[maxn], y[maxn];

int main(){
  freopen("berlin52.tsp", "r", stdin);
  freopen("in", "w", stdout);
  int n;
  cin>>n;
  
  //~ cout<<n<<endl;
  for(int i = 1; i <= n; i++){
    int q;
    cin>>q>>x[i]>>y[i];
    //~ cout<<q<<' '<<x[i]<<' '<<y[i]<<endl;
  }  
  
  for(int i = 1; i <= n; i++){
    for(int j = i+1; j <= n; j++){
      cout<<i<<' '<<j<<' '<<(int)hypot(x[i]-x[j],y[i]-y[j] )<<endl;
    }
  }
}
