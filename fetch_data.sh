if [ "$1" = "debug" ] ; then
    bash downloads.curl
else
    cat downloads.curl | sort -R | parallel -j 0
fi

cat logs/* > errors
