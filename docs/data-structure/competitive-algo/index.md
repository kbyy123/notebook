# 算法竞赛

!!! abstract "概要"

    + 时间：2025/10 - 2026/1
    + 课程：[Acwing 算法基础课](https://www.acwing.com/activity/content/11/)
    + 参考材料：
    	+ [OI Wiki](https://oi-wiki.org/)
    	+ [Algorithms for Competitive Programming](https://cp-algorithms.com/)
    
!!! info "说明"

    大一上学习算法竞赛的笔记．因为最近要准备校赛和蓝桥杯（不过大概率是重在参与），翻出来复习顺便写一下笔记．

!!! quote "常用模板"

    ```cpp
    // 常用头文件
    #include <iostream>
    #include <algorithm>
    #include <cstring>

    // 万能头
    #include <bits/stdc++.h>

    // 取消同步流
    ios::sync_with_stdio(0), cin.tie(0), cout.tie(0);

    // 简写
    using ll = long long;
    using PII = pair<int, int>;

    // 链式前向星（不带权）
    int h[N], e[M], ne[M], idx = 1;

    void add(int a, int b)
    {
        e[idx] = b;
        ne[idx] = h[a];
        h[a] = idx++;
    }

    // 链式前向星（带权）
    int h[N], e[M], ne[M], w[M], idx = 1;

    void add(int a, int b, int c)
    {
        e[idx] = b;
        w[idx] = c;
        ne[idx] = h[a];
        h[a] = idx++;
    }

    // 排序去重
    sort(X.begin(), X.end());
    X.erase(unique(X.begin(), X.end()), X.end());
    ```