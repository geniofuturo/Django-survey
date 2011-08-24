Ext.ns('Survey.Data', 'Survey.UI', 'Survey.Handler');
//------------------------------------------
// datastore
//------------------------------------------


//------------------------------------------
//ui
//------------------------------------------

Survey.UI.QuestionDetails = function() {
    var form = Ext.ComponentMgr.create({
        xtype: 'dynform',
        disabled: true,
        title: gettext('Details'),
        region: 'center',
        autoScroll: true,
        id: 'question-details'
    });
    Ext.ux.msgBus.subscribe('question.selected', function(survey_id, question_id) {
        var url = String.format('/betatest/survey/api/surveys/{0}/questions/{1}.form', survey_id, question_id);
        params = {
        };
        form.setDisabled(false);
        form.updateData(form, question_id, url, params);
    });
    Ext.ux.msgBus.subscribe('question.deselected', function() {
    	form.setDisabled(true);
    });
    
    return form;
}
