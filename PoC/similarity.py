def calculate_levenshtein_distance(s1, s2):
    m = len(s1)
    n = len(s2)

    #Initializing 2d grid with zeros
    matrix = [[0 for i in range(n+1)] for i in range(m+1)]

    for i in range(m+1):
        matrix[i][0] = i #0th column
    for j in range(n+1):
        matrix[0][j] = j #0th row

    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1].lower() == s2[j-1].lower():
                matrix[i][j] = matrix[i-1][j-1]
            else:
                matrix[i][j] = 1 + min(matrix[i][j-1], matrix[i-1][j], matrix[i-1][j-1])
    return matrix[m][n]
def calculate_similarity_score(query, sentence):
    distance = calculate_levenshtein_distance(query, sentence)
    max_len = max(len(query), len(sentence))
    similarity = 1.0 - distance/max_len 
    return max(0.0, similarity)
ans = calculate_similarity_score("matas","ratas")
print(ans)
