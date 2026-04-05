# 基础算法
## 排序
### 归并排序求逆序对
题目链接：[788. 逆序对的数量](https://www.acwing.com/problem/content/790/)

归并排序因其分治特性，能够在排序过程中求得一些数据，这也是它比快排强的地方．

不妨规定归并排序的返回值是 $[l, r]$ 区间内的逆序对数量，则其由三部分组成：
1. 左半部分 $[l, mid]$ 的逆序对数量；
2. 右半部分 $[mid+1, r]$ 的逆序对数量；
3. 跨越左右两部分的逆序对数量。

前面两个部分我们可以用递归 `merge_sort(l, mid)` 和 `merge_sort(mid + 1, r)` 来计算，后半部分我们可以在排序的过程中统计．由于左半边每一个元素的下标均小于右半边的元素并且两边均已排序，因此当我们发现 `a[i] <= a[j]` 时，说明 `a[i]` 不会与右半边后续的元素构成逆序对，可以直接将其放入临时数组中；但当我们发现 `a[i] > a[j]` 时，说明 `a[j]` 会与左半边从 `i` 到 `mid` 的所有元素构成逆序对，因此可以将逆序对数量增加 `mid - i + 1`．

???+ code "代码"

    时间复杂度 $O(n\log n)$．
    ```cpp
    #include <iostream>
    #include <algorithm>
    #include <cstring>
    using namespace std;
    using ll = long long;
    const int N = 1e5 + 9;

    int n;
    int a[N], tmp[N];

    ll merge_sort(int l, int r)
    {
        if (l >= r)
            return 0;
        int mid = l + r >> 1;
        ll ans = merge_sort(l, mid) + merge_sort(mid + 1, r);
        
        int i = l, j = mid + 1, k = l;
        while (i <= mid && j <= r)
        {
            if (a[i] <= a[j])
                tmp[k++] = a[i++];
            else 
            {
                ans += mid - i + 1;
                tmp[k++] = a[j++];
            }
        }
        
        while (i <= mid)
            tmp[k++] = a[i++];
        while (j <= r)
            tmp[k++] = a[j++];
        for (int i = l; i <= r; i++)
            a[i] = tmp[i];
        return ans;
    }

    int main()
    {
        ios::sync_with_stdio(0), cin.tie(0), cout.tie(0);
        cin >> n;
        for (int i = 1; i <= n; i++)
            cin >> a[i];
        cout << merge_sort(1, n);
        return 0;
    }
    ```

## 二分
### 整数二分
题目链接：[789. 数的范围](https://www.acwing.com/problem/content/791/)

本题需要找到一个数在有序数组中的起始位置和终止位置，可以使用二分查找来实现；由于二分查找每次只能找到一个位置，因此需要分别进行两次二分查找：一次查找起始位置，一次查找终止位置．记住二分查找的模板，初始时 `l`，`r` 分别位于超出数组的两端，终止条件是 `l + 1 == r` ，也就是说结束时 `l` 和 `r` 其中一个会满足临界条件．

以 `if (a[mid] < x) l = mid; else r = mid;` 为例，每次更新的 `l` 都是小于 `x` 的，`r` 都是大于等于 `x` 的，因此最后结束时 `l,r` 相邻，得到 `l` 是最大的小于 `x` 的数，`r` 是最小的大于等于 `x` 的数。．

???+ code "代码"

    时间复杂度 $O(q\log n)$．
    ```cpp
    #include <iostream>
    #include <algorithm>
    #include <cstring>
    using namespace std;
    using ll = long long;
    const int N = 1e5 + 9;

    int n, q;
    int a[N];

    int main()
    {
        ios::sync_with_stdio(0), cin.tie(0), cout.tie(0);
        cin >> n >> q;
        for (int i = 0; i < n; i++)
            cin >> a[i];
        while (q--)
        {
            int x; 
            cin >> x;
            
            // 找左临界 
            int l = -1, r = n;
            while (l + 1 != r)
            {
                int mid = l + r >> 1;
                if (a[mid] < x) l = mid;
                else r = mid;
            }
            cout << (a[r] == x ? r : -1) << ' ';
            
            // 找右临界 
            l = -1, r = n;
            while (l + 1 != r)
            {
                int mid = l + r >> 1;
                if (a[mid] > x) r = mid;
                else l = mid;
            }
            cout << (a[l] == x ? l : -1) << ' ';
            cout << '\n';
        }
        return 0;
    }
    ```

## 高精度
### 高精度加法
题目链接：[791. 高精度加法](https://www.acwing.com/problem/content/793/)
用字符串存储两个整数并从低位到高位存入数组中（这样最后的进位直接在最后 `push_back` 即可），然后从低位到高位逐位模拟加法过程，并存储进位．

???+ code "代码"

    时间复杂度 $O(\max(l_a,l_b))$．
    ```cpp
    #include <iostream>
    #include <algorithm>
    using namespace std;
    using ll = long long;
    const int N = 1e5 + 9;

    vector<int> A, B;

    vector<int> add(vector<int> &A, vector<int> &B)
    {
        vector<int> C;
        int t = 0;
        for (int i = 0; i < A.size() || i < B.size(); i++)
        {
            if (i < A.size())
                t += A[i];
            if (i < B.size())
                t += B[i];
            C.push_back(t % 10);
            // 进位
            t /= 10;
        }
        // 将剩余未进位的 t 进位
        while (t)
        {
            C.push_back(t % 10);
            t /= 10;
        }
        // 删去前导零
        while (C.size() > 1 && C.back() == 0)
            C.pop_back();
        return C;
    }

    int main()
    {
        ios::sync_with_stdio(0), cin.tie(0), cout.tie(0);
        string a, b;
        cin >> a >> b;
        for (int i = a.size() - 1; i >= 0; i--)
            A.push_back(int(a[i] - '0'));
        for (int i = b.size() - 1; i >= 0; i--)
            B.push_back(int(b[i] - '0'));
        auto C = add(A, B);
        for (int i = C.size() - 1; i >= 0; i--)
            cout << C[i];
    }
    ```

### 高精度减法
题目链接：[792. 高精度减法](https://www.acwing.com/problem/content/794/)

类似高精度加法，只不过此时的进位变成了结尾，t的可能取值从0，1变成了0，-1．为了防止出现减数比被减数大而计算结果为负数的情况，我们写一个 `cmp` 函数判断两个数的大小，如果减数比被减数大就先输出一个负号，然后调换做减法．

???+ code "代码"

    时间复杂度 $O(\max(l_a,l_b))$．
    ```
    #include <iostream>
    #include <algorithm>
    using namespace std;
    using ll = long long;
    const int N = 1e5 + 9;

    vector<int> A, B;

    bool cmp(vector<int> &A, vector<int> &B)
    {
        if (A.size() != B.size())
            return A.size() > B.size();
        for (int i = A.size() - 1; i >= 0; i--)
            if (A[i] != B[i])
                return A[i] > B[i];
        return true;
    }

    vector<int> sub(vector<int> &A, vector<int> &B)
    {
        vector<int> C;
        int t = 0;
        for (int i = 0; i < A.size(); i++)
        {
            t += A[i];
            if (i < B.size())
                t -= B[i];
            if (t >= 0)
            {
                C.push_back(t);
                t = 0;
            }
            else
            {
                C.push_back(t + 10);
                t = -1;
            }
        }
        while (t)
        {
            C.push_back(t % 10);
            t /= 10;
        }
        while (C.size() > 1 && C.back() == 0)
            C.pop_back();
        return C;
    }

    int main()
    {
        ios::sync_with_stdio(0), cin.tie(0), cout.tie(0);
        string a, b;
        cin >> a >> b;
        for (int i = a.size() - 1; i >= 0; i--)
            A.push_back(a[i] - '0');
        for (int i = b.size() - 1; i >= 0; i--)
            B.push_back(b[i] - '0');

        if (cmp(A, B))
        {
            auto C = sub(A, B);
            for (int i = C.size() - 1; i >= 0; i--)
                cout << C[i];
        }
        else
        {
            auto C = sub(B, A);
            cout << '-';
            for (int i = C.size() - 1; i >= 0; i--)
                cout << C[i];
        }
    }
    ```