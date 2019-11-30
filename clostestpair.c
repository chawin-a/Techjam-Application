#include<stdio.h>
#include<math.h>
#include<stdlib.h>
#include<float.h>
double MIN;
typedef struct
{
   double x,y;
}P;
P a[500500];
P tmp[500500];
double min(double a,double b)
{
    return (a<b)?a:b;
}
int cmpx(const void *a,const void *b)
{
    P *r,*s;
    r=(P*)a;
    s=(P*)b;
    if(r->x>s->x)return 1;
    else return -1;
}
int cmpy(const void *a,const void *b)
{
    P *r,*s;
    r=(P*)a;
    s=(P*)b;
    if(r->y>s->y)return 1;
    else return -1;
}
double sol(int x,int y)
{
    double t1=a[x].x-a[y].x;
    double t2=a[x].y-a[y].y;
    return sqrt(t1*t1+t2*t2);
}
double soltmp(int x,int y)
{
    double t1=tmp[x].x-tmp[y].x;
    double t2=tmp[x].y-tmp[y].y;
    return sqrt(t1*t1+t2*t2);
}
double closest_pair(int left,int right)
{
    int i,j,k=0;
    double d=DBL_MAX;
    if(left==right)return d;
    if(left+1==right)return sol(left,right);
    int mid=(left+right)/2;
    double d1=closest_pair(left,mid);
    double d2=closest_pair(mid+1,right);
    d=min(d1,d2);
    for(i=left;i<=right;i++)
    {
        if(fabs(a[mid].x-a[i].x)<=d)tmp[k++]=a[i];
    }
    qsort(tmp,k,sizeof(P),cmpy);
    for(i=0;i<k;i++)
    {
        for(j=i+1;j<k&&tmp[j].y-tmp[i].y<d;j++)
        {
            double d3=soltmp(i,j);
            if(d-d3>1e-9)d=d3;
        }
    }
    return d;

}
int main()
{
    FILE  *fp = fopen("in", "r");
    int n,i;
    fscanf(fp,"%d",&n);
    for(i=0;i<n;i++)
    {
        fscanf(fp,"%lf %lf",&a[i].x,&a[i].y);
    }
    qsort(a,n,sizeof(P),cmpx);
    MIN=closest_pair(0,n-1);
    printf("%lf\n",MIN);
    return 0;
}
