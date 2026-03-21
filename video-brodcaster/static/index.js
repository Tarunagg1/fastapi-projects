const getDevice = async () => {
    // fetch('/devices')
    //     .then(response => response.json())
    //     .then(data => {
    //         const select = document.getElementById('camera');
    //         select.innerHTML = '';
    //         data.devices.forEach(device => {
    //             const option = document.createElement('option');
    //             option.value = device.id;
    //             option.text = device.label || `Camera ${select.length + 1}`;
    //             select.appendChild(option);
    //         });
    //     })

    let data = {
        devices: [
            { id: 'device1', label: 'Camera 1' },
            { id: 'device2', label: 'Camera 2' }
        ]
    }
    const select = document.getElementById('camera');
    select.innerHTML = '';
    data.devices.forEach(device => {
        const option = document.createElement('option');
        option.value = device.id;
        option.text = device.label || `Camera ${select.length + 1}`;
        select.appendChild(option);

    });
}
const startStream = async () => {
}


const stopStream = async () => {
}
