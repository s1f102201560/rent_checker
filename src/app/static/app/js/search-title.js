$(document).ready(function () {
  function extractLastSegment(url) {
    const parts = url.split('/');
    return parts[parts.length - 1] || parts[parts.length - 2];
  }
  function navigateToChat(roomLinkSegment) {
    window.location.href = `/consultation/${roomLinkSegment}/`;
  }
  function openDeleteModal(consultationId) {
    if (confirm('この相談を削除してもよろしいですか？')) {
        window.location.href = `/consultation_delete/${consultationId}/`;
    }
  }

  $('#search-form').on('input', function (e) {
    e.preventDefault();

    var query = $('#id_query').val();

    $.ajax({
      url: window.searchConsultationsUrl,
      type: "GET",
      data: {
        'query': query
      },
      dataType: 'json',
      success: function (data) {
        var tbody = '';
        data.consultations.forEach(function(consultation) {
          tbody += '<tr class="bg-white border-b border-gray-300">' +
          '<td class="px-6 py-4">' +
              '<input type="checkbox" name="consultations" value="' + consultation.id + '" class="rounded border-gray-300">' +
          '</td>' +
          '<td class="px-6 py-4 font-medium text-gray-600 whitespace-nowrap">' + consultation.title + '</td>' +
          '<td class="px-6 py-4">' +
              '<a href="/consultation/' + extractLastSegment(consultation.room_link) + '" ' +
                  'onclick="navigateToChat(\'' + extractLastSegment(consultation.room_link) + '\')" ' +
                  'class="text-blue-400 hover:underline break-all">' +
                  consultation.room_link +
              '</a>' +
          '</td>' +
          '<td class="px-6 py-4">' + consultation.file + '</td>' +
          '<td class="px-6 py-4">' + consultation.checklist + '</td>' +
          '<td class="px-6 py-4">' + consultation.created_at + '</td>' +
          '<td class="px-3 py-4">' +
              '<a href="/consultation_detail/' + consultation.id + '" class="text-blue-400 hover:underline">詳細</a>' +
          '</td>' +
          '<td class="px-3 py-4">' +
              '<a href="/consultation_edit/' + consultation.id + '" class="text-green-400 hover:underline">編集</a>' +
          '</td>' +
          '<td class="px-3 py-4">' +
              '<button type="button" class="font-semibold text-red-400 hover:underline" ' +
                      'onclick="openDeleteModal(\'' + consultation.id + '\')">' +
                  '削除' +
              '</button>' +
          '</td>' +
        '</tr>';
        });
        $('#search-results tbody').html(tbody);
      },
      error: function (xhr, status, error) {
        console.error('検索に失敗しました:', error);
      }
    });
  });
});