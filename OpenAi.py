
import openai
import os
key = "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"

init_prompt = """You are an expert programmer, and you are trying to summarize a "git diff" file .
Reminders about the git diff format:
For each file, there are a few metadata lines, for example:
\`\`\`
diff --git a/lib/index.js b/lib/index.js
index aadf691..bfef603 100644
--- a/lib/index.js
+++ b/lib/index.js
\`\`\`
This means that \`lib/index.js\` was modified in this commit. Note that this is only an example.
Then there is a specifier of the lines that were modified.
A line starting with \`+\` means it was added.
A line that starting with \`-\` means that line was deleted.
A line that starts with neither \`+\` nor \`-\` is code given for context and better understanding. 
This is not part of the diff.
`
"""

injection_prompt = """The following is a git diff of a single file.
Please summarize it in a comment, describing the changes made in the diff in high level.
Do it in the following way:
Write \`SUMMARY:\` and then write a summary of the changes made in the diff, as a bullet point list.
Every bullet point should start with a \`*\`. :"""



class OpenAI:

    def __init__(self, api_key):

        openai.api_key = "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"
        #openai.organization = "ma-org"
        #openai.api_key = api_key
        #Authorization: Bearer YOUR_API_KEY


    def generate_response(self, prompt):
        try:
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=prompt,
                temperature=0.8,
                max_tokens=1024
            )
            return response["choices"][0]["text"]
        except openai.error.OpenAIError as error:
            print(f"Error generating response: {error}")
def test():

    openai = OpenAI(key)
    prompt = init_prompt + injection_prompt + """

    @@ -1,18 +1,18 @@
-class SelfAPI {
-    constructor() {
-        this.status = "in progress";
-    }
-
-    async fetchData() {
-        //make api call and update the status
-        this.status = await API.fetchData();
-        return this.status;
-    }
-
-    render() {
-        //update the dom with the status
-        document.getElementById("status").innerHTML = this.status;
-    }
-}
-
-const selfApi = new SelfAPI();
\ No newline at end of file
+# class SelfAPI {
+#     constructor() {
+#         this.status = "in progress";
+#     }
+#
+#     async fetchData() {
+#         //make api call and update the status
+#         this.status = await API.fetchData();
+#         return this.status;
+#     }
+#
+#     render() {
+#         //update the dom with the status
+#         document.getElementById("status").innerHTML = this.status;
+#     }
+# }
+#
+# const selfApi = new SelfAPI();
\ No newline at end of file
"""

    response = openai.generate_response(prompt)
    if response:
        print(response)


def check_response(response):
    pass


def generate_PR_summery(diffs):
    openai = OpenAI(key)
    prompt = init_prompt
    final_summery = ""

    for diff in diffs:
        prompt += injection_prompt + diff
        response = openai.generate_response(prompt)

        check_response(response) #TODO: check if the response is good
        if response:
            final_summery += response





test()
