%%writefile download_models.sh
#!/bin/bash

# Create the models directory (relative path)
mkdir -p models

echo "Downloading models from Dropbox into the 'models' directory..."

# Download models and check if the download was successful
if wget -O Models/Line_detection_weights.pt "https://www.dropbox.com/scl/fi/rgvdk78h21usxid1dr2wr/Line_detection_weights-best.pt?rlkey=ne1ikondiraa8lxxe02454kjm&st=ts45bc36&dl=1"; then
    echo "Line_detection_weights.pt downloaded successfully."
else
    echo "Failed to download Line_detection_weights.pt"
fi

if wget -O Models/People_detection_weights.pt "https://www.dropbox.com/scl/fi/0ysczx7b0nj6r8ubapp30/People_detection_weights-best.pt?rlkey=f79wmefyidbl6z2emaz342nfa&st=fuy9xbpc&dl=1"; then
    echo "People_detection_weights.pt downloaded successfully."
else
    echo "Failed to download People_detection_weights.pt"
fi

echo "Download process completed."