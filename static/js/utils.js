/**
 * Created by mac on 2/18/18.
 */

disableddates =[]
function DisableSpecificDates(date) {
    console.log(disableddates);
    var string = jQuery.datepicker.formatDate('dd-mm-yy', date);
    return [disableddates.indexOf(string) == -1];
}
