function limit_len(element)
{
    const max_len = 255;

    if(element.value.length > max_len) {
        element.value = element.value.substr(0, max_len);
    }
}