document.addEventListener('DOMContentLoaded', function () {
    const tableBody = document.getElementById('items-tbody');
    const form = document.getElementById('cotizacion-form');
    const downloadButtonsArea = document.getElementById('download-buttons-area');

    function formatCurrency(value) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(value);
    }

    function hideDownloadButtons() {
        downloadButtonsArea.style.display = 'none';
    }

    function showDownloadButtons() {
        downloadButtonsArea.style.display = 'inline-block';
    }

    function updateTotals() {
        hideDownloadButtons();
        let totalGeneral = 0;
        tableBody.querySelectorAll('tr').forEach(row => {
            const cantidad = parseFloat(row.querySelector('[name="cantidad"]').value) || 0;
            const precio = parseFloat(row.querySelector('[name="precio"]').value) || 0;
            const totalFila = cantidad * precio;
            row.querySelector('.item-total').value = formatCurrency(totalFila);
            totalGeneral += totalFila;
        });
        document.getElementById('total-general').textContent = formatCurrency(totalGeneral);
    }

    tableBody.addEventListener('input', function(e) {
        if (e.target.classList.contains('item-calc')) updateTotals();
    });

    tableBody.addEventListener('click', function(e) {
        if (e.target.closest('.remove-row')) {
            if (tableBody.querySelectorAll('tr').length > 1) {
                e.target.closest('tr').remove();
                updateTotals();
            }
        }
    });

    function createFirstRow() {
        hideDownloadButtons();
        const firstRowHTML = `
            <tr>
                <td><input type="text" class="form-control" name="descripcion" placeholder="Descripción del servicio o producto"></td>
                <td><input type="number" class="form-control item-calc" name="cantidad" value="1" min="1"></td>
                <td><input type="number" class="form-control item-calc" name="precio" placeholder="0.00" step="0.01" min="0"></td>
                <td><input type="text" class="form-control item-total" readonly value="$0.00"></td>
                <td><button type="button" class="btn btn-danger btn-sm remove-row"><i class="bi bi-trash"></i></button></td>
            </tr>
        `;
        tableBody.innerHTML = firstRowHTML;
    }

    document.getElementById('add-row-btn').addEventListener('click', function() {
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td><input type="text" class="form-control" name="descripcion" placeholder="Descripción del servicio o producto"></td>
            <td><input type="number" class="form-control item-calc" name="cantidad" value="1" min="1"></td>
            <td><input type="number" class="form-control item-calc" name="precio" placeholder="0.00" step="0.01" min="0"></td>
            <td><input type="text" class="form-control item-total" readonly value="$0.00"></td>
            <td><button type="button" class="btn btn-danger btn-sm remove-row"><i class="bi bi-trash"></i></button></td>
        `;
        tableBody.appendChild(newRow);
        hideDownloadButtons();
    });

    document.getElementById('fecha').valueAsDate = new Date();
    createFirstRow();
    updateTotals();

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const items = [];
        tableBody.querySelectorAll('tr').forEach(row => {
            const descripcion = row.querySelector('[name="descripcion"]').value;
            if (descripcion) {
                items.push({
                    descripcion: descripcion,
                    cantidad: parseFloat(row.querySelector('[name="cantidad"]').value),
                    precio: parseFloat(row.querySelector('[name="precio"]').value)
                });
            }
        });

        const cotizacionData = {
            cliente: document.getElementById('cliente').value,
            fecha: document.getElementById('fecha').value,
            estado: document.getElementById('estado').value,
            notas: document.getElementById('notas').value,
            items: items,
            total: document.getElementById('total-general').textContent
        };

        fetch('/guardar-cotizacion', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(cotizacionData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                alert(data.message);
                
                const pdfLink = document.getElementById('pdf-download-link');
                const excelLink = document.getElementById('excel-download-link');
                
                pdfLink.href = `/descargar-pdf/${data.cotizacion_id}`;
                excelLink.href = `/descargar-excel/${data.cotizacion_id}`;
                
                showDownloadButtons();
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    });
});