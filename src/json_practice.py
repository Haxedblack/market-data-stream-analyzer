import json 
# create some sample data 
user = {
    'name' : 'HaxedBlack',
    'age' : 19,
    'skills' : ["Python","Git","CLI Tools"],
    'is_active': True
}
#saving
with open("output/user.json", 'w') as f:
    json.dump(user,f,indent = 2)
print('user.json saved!')
#reading
with open("output/user.json",'r') as f:
    loaded_user = json.load(f)
print('Loaded from file:')
print(loaded_user)
#modifying
loaded_user['skills'].append('Argparse')
#saving after modification
with open("output/user.json", 'w') as f:
    json.dump(user,f,indent = 2)