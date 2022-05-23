first=('0' '1' '2' '3' '4' '5' '6' '7' '8' '9' 'A' 'B' 'C' 'D' 'E' 'F')
second=('0' '1' '2' '3' '4' '5' '6' '7' '8' '9' 'A' 'B' 'C' 'D' 'E' 'F')

for i in ${first[@]}; 
    do
        for j in ${second[@]}; 
            do
                mkdir -p /Volumes/Samsung_T5/KnowYourPassword/KnowYourPasswordApi/Database/Passwords/rockyou2/$i/
                sed 's/^.\{2\}//g' /Volumes/Samsung_T5/KnowYourPassword/KnowYourPasswordApi/Database/Passwords/rockyou/hashes/$i/passwords-starting-with-$i$j.txt >> /Volumes/Samsung_T5/KnowYourPassword/KnowYourPasswordApi/Database/Passwords/rockyou2/$i/passwords-starting-with-$i$j.txt
            done
    done