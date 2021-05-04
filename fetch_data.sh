if [ "$1" = "debug" ] ; then
    bash downloads.curl
else
    cat downloads.curl | sort -R | parallel -j100
fi

cat logs/* > errors
