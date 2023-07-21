import React from 'react';

function Hello({name, color, isSpecial }) {
    return (
        <div style={{ color }}>
        {isSpecial && <b> * </b>}
        Hello~!! {name}</div>
    )
}

Hello.defaulProps = {
    name: 'NoName'
}

export default Hello;