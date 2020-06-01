### Krunner shell

return shell output
can run commands

---

### configure

all in bash file `~/.config/krunnershell.sh`


create actions
In krunner run `action:`

In bash file create one or two function for one action
 - match_action() {...}    return text list
 - run_action() {...}      optional, click on line

example: action "ls" in krunner: "ls:/etc/"

```
match_ls(){
  # return list
  [ -z "$1" ] && exit 0
  [[ ${#1} < 2 ]] && exit 0
  match="${1}*"
  ls -dHp -1 $match --color=never
}
run_ls (){
  xdg-open "$1"
}
```

or only display with action `df:`
```
match_df() {
  df | awk '/^\// {print $1"\t"$5" "$(NF)}'
}
```


---

### install

After install run `kquitapp5 krunner` if not reboot
