# Get the commit message
commit_message = open('.git/COMMIT_EDITMSG', 'r').read()

# Append "Hello World" to the commit message
new_commit_message = commit_message + '\nHello World'

# Write the new commit message back to the file
with open('.git/COMMIT_EDITMSG', 'w') as f:
    f.write(new_commit_message)
