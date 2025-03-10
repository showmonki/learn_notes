from typing import List
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        result = []
        p = ['(',')'] * n
        v = {'(':1,')':-1}
        m = {ii:val for ii,val in enumerate(p)}

        
        def backtrack(path):
            if len(path)==n*2:
                # print(path)
                print([m[sub]for sub in path])
            # if (len(path)==6) & (sum([v[sub]for sub in path])==0):
                result.append([m[sub]for sub in path])
            
            
            for ii in range(n*2):
                if ii not in path:
                    path.append(ii)
                    pattern_trim = [jj[:len(path)] for jj in result] if result else []
                    if (sum([v[m[sub]]for sub in path])>=0) & ([m[sub]for sub in path] not in pattern_trim):
                        print(path,[m[sub]for sub in path],'==',result)
                        backtrack(path)
                    path.pop()
                    
        backtrack([])

        return [''.join(ii) for ii in result]

# Example Usage
s = Solution()
print(s.generateParenthesis(3))