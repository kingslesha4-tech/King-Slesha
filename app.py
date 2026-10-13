function pagar(){
  // Agora o valor vai para 853772668
  fetch('https://api.e2payments.mz/v1/c2b', {
    numero_cliente: document.getElementById('mpesa').value, // quem paga
    numero_recebedor: "853772668", // TU - King Slesha
    valor: 50,
    referencia: "CALY-FILME-48H"
  })
}
