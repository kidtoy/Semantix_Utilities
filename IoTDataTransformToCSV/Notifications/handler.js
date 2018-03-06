'use strict';

module.exports.convert = (event, context, callback) => {
    let success = 0; // Number of valid entries found
    let failure = 0; // Number of invalid entries found

    /* Process the list of records and transform them */
    const output = event.records.map((record) => {
        const entry = (Buffer.from(record.data, 'base64')).toString('utf8');
        var JSONentry = JSON.parse(entry)
        const result = `${JSONentry.person},${JSONentry.mac_address},${JSONentry.date_time_sensor},${JSONentry.section},${JSONentry.id_deploy},${JSONentry.branch},${JSONentry.sentiment},${JSONentry.score},${JSONentry.date_time}`;
        console.log("Logging Result = "+result)
        if (result) {
            /* Prepare CSV version from Apache log data */
            const payload = (Buffer.from(JSON.stringify(result), 'utf8')).toString('base64');
            console.log("Logging payload = "+payload)
            success++;
            return {
                'recordId': record.recordId,
                'result': 'Ok',
                'data': payload+"\n",
            };
        } else {
            /* Failed event, notify the error and leave the record intact */
            failure++;
            return {
                'recordId': record.recordId,
                'result': 'ProcessingFailed',
                'data': record.data,
            };
        };
    });
    console.log(`Processing completed.  Successful records ${success}, Failed records ${failure}.`);
    callback(null, { 'records': output });
};
