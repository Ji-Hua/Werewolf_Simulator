mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"michaelhua1993@foxmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml