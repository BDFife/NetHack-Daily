# This script assumes you've already created the .cmd and .nss files.
# FIXME: Need to check to see if the nethack savegame file exists before trying to copy it. 

turn_num=$1

# Check to see if the the previous turn exists.
# Keep decrementing until a match is found.
dec_turn=`expr $turn_num - 1`
until [ -e "$dec_turn.tip" ]; do
    echo "turnfiles for $dec_turn not found."
    dec_turn=`expr $dec_turn - 1` 
done

echo "Using $dec_turn as the reference turn."

savegame_loc="/usr/games/lib/nethackdir/save/501Cody.Z"
savegame_file="_501Cody.Z"

# These are the files that are pre-requisites for the script to run.
# They are not used by the script, but this rule is in place as 
# a best practice. 
prereq_files=( $turn_num.cmd $turn_num.nss $savegame_loc)

for file in ${prereq_files[@]}; do
    if [ ! -e "$file" ] 
        then echo "$file is missing. Add this before you run the script."; exit 1
    fi 
done


# These are the files from the previous turn that 
# are needed for the rest of this script to work.
#required_files=( $dec_turn.obj $dec_turn.inv $savegame_loc )
required_files=( $dec_turn.obj $dec_turn.inv )

for file in ${required_files[@]}; do
    if [ ! -e "$file" ]
        then echo "$file is missing. Aborting script."; exit 1
    fi
done

# These are the files that the script needs to create.
# Abort if they exist.
new_files=( $turn_num$savegame_file $turn_num.inv $turn_num.obj $turn_num.str $turn_num.tip )

for file in ${new_files[@]}; do
    if [ -e "$file" ] 
        then echo "$file is already present. Aborting script."; exit 1
    fi
done

# Copy the savegame file into the main folder. 
cp $savegame_loc $turn_num$savegame_file
#echo "Skipping the savegame copy for now. FIX!FIX!FIX!"
#echo $turn_num$savegame_file

# Create the tip and story.
echo "Brian to write tip." > $turn_num.tip
echo "Paul to write story." > $turn_num.str

# Copy over the obj and inv files. 
cp $dec_turn.inv $turn_num.inv
cp $dec_turn.obj $turn_num.obj

# Finished.
echo "All files have been copied or created."
echo "Make sure to update $turn_num.inv and $turn_num.obj"
