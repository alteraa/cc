from compiler import ChatCompiler

reflections = {
    "ben": "sen",
    "benim": "senin",
    "bence": "sence",
    "sen": "ben",
    "senin": "benim",
    "sence": "bence",
}
cc = ChatCompiler('chat.json', reflections)

print(
    cc.respond("alternatif akım nedir?")
)