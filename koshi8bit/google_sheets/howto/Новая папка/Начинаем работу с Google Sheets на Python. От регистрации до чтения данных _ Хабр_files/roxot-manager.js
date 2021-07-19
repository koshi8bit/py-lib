(function (c) {
    if (isEngineInited()){
        return;
    }

    let script = document.createElement('script');
    script.type = 'text/javascript';
    script.async = 1;
    script.src = c.managerUrl;
    script.dataset.roxotInited = 'true';

    let head = document.getElementsByTagName('head')[0];
    head.insertBefore(script, head.firstChild);

    window.rom = window.rom || {cmd: [], icmd: []};
    window.rom.icmd = window.rom.icmd || [];
    window.rom.icmd.push(c);

    function isEngineInited(){
        return  document.querySelectorAll('[data-roxot-inited]').length;
    }
})({"adBlockMode":"iframe","managerUrl":"https:\/\/cdn-plus.roxot-panel.com\/wrapper\/js\/common-engine.js?v=s-f330b9da-a14f-4153-9834-dc7586fe0de4","wrapperUrl":"https:\/\/cdn-plus.roxot-panel.com\/wrapper\/js\/wrapper.js?v=s-f330b9da-a14f-4153-9834-dc7586fe0de4","placementConfigTemplate":"https:\/\/cdn-plus.roxot-panel.com\/wrapper-builder\/placement\/__PLACEMENT_ID__?v=d-fdeeb026-9018-4dcf-ac37-e3cc3f96a9be","isLanguageSpecific":false,"hostConfig":{"habr.com":{"wrapperOptions":[]}},"isBrowserSpecific":false,"isOsSpecific":false,"isDeviceTypeSpecific":false,"dynamicUrlTemplate":"","wrapperConfig":{"engineFileName":"roxot-common-engine.js","universalPlaceHolder":{"enabled":false},"prebid":{"adjustment":{"adriver":0.95,"appnexus":0.95,"between":0.95,"criteo":0.75,"getintent":0.6,"mytarget":0.2,"otm":0.95,"rtbhouse":0.6,"rubicon":0.95,"sovrn":1,"vox":0.9},"path":"https:\/\/cdn-plus.roxot-panel.com\/wrapper\/js\/prebid.js?v=s-f330b9da-a14f-4153-9834-dc7586fe0de4"},"adfox":{"hb":{"biddersMap":{"betweenDigital":"1471719","myTarget":"1471718","otm":"1471725","segmento":"1496136","hybrid":"1505514","adriver":"1508036","rtbhouse":"1393902","criteo":"1393905","getintent":"1393904","videonow":"1407059"},"timeout":1000}},"prebidAnalyticsIntegration":{"enabled":true,"publisherId":"92707dda-5614-4d3a-b4f5-531645d13ecf","auctionSettings":{"isNeedToSend":true,"sampleCoefficient":10},"impressionSettings":{"isNeedToSend":true,"sampleCoefficient":10}}},"lazyLoading":[]})