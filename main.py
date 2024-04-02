import heapq
from collections import Counter, defaultdict

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    # Contagem de frequência de caracteres no texto
    frequency = Counter(text)
    # Cria uma fila de prioridade inicial com os nós dos caracteres e suas frequências
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        # Extrai os dois nós de menor frequência da fila de prioridade
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        # Combina os dois nós para formar um novo nó
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        # Coloca o novo nó de volta na fila de prioridade
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def generate_huffman_codes(root, code='', mapping=defaultdict()):
    if root:
        if not root.left and not root.right:
            # Se o nó atual é uma folha, atribui o código Huffman ao caractere correspondente
            mapping[root.char] = code
        # Percorre a árvore à esquerda com o código '0'
        generate_huffman_codes(root.left, code + '0', mapping)
        # Percorre a árvore à direita com o código '1'
        generate_huffman_codes(root.right, code + '1', mapping)
    return mapping

def encode(text, mapping):
    # Codifica o texto usando a tabela de mapeamento de Huffman
    encoded_text = ''.join(mapping[char] for char in text)
    return encoded_text

def decode(encoded_text, root):
    decoded_text = ''
    current_node = root
    for bit in encoded_text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if not current_node.left and not current_node.right:
            # Se chegamos a uma folha, adiciona o caractere correspondente ao texto decodificado
            decoded_text += current_node.char
            # Reinicia a busca da raiz
            current_node = root

    return decoded_text

def ascii_length(text):
    # Calcula o comprimento da representação ASCII do texto
    return len(text) * 8

def huffman_length(encoded_text, mapping):
    # Calcula o comprimento da representação codificada de Huffman
    return len(encoded_text)

def compression_ratio(text, encoded_text, mapping):
    ascii_len = ascii_length(text)
    huffman_len = huffman_length(encoded_text, mapping)
    return ascii_len / huffman_len

def huffman_encoding_decoding(text):
    root = build_huffman_tree(text)
    mapping = generate_huffman_codes(root)
    encoded_text = encode(text, mapping)
    decoded_text = decode(encoded_text, root)
    return encoded_text, decoded_text, mapping

# main:
text = input("Qual a frase a ser usada?  ")
encoded_text, decoded_text, mapping = huffman_encoding_decoding(text)
print("\nTexto original:", text)
print("Código criptografado Huffman:", encoded_text)
print("Texto descriptografado:", decoded_text)
print("Taxa de compressão comparada ao formato ASCII:", compression_ratio(text, encoded_text, mapping))
