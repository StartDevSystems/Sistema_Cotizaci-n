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
        if (downloadButtonsArea) downloadButtonsArea.style.display = 'none';
    }

    function showDownloadButtons() {
        if (downloadButtonsArea) downloadButtonsArea.style.display = 'block';
    }

    function updateTotals() {
        hideDownloadButtons();
        let totalGeneral = 0;
        tableBody.querySelectorAll('tr').forEach(row => {
            const cantidadInput = row.querySelector('[name="cantidad"]');
            const precioInput = row.querySelector('[name="precio"]');
            const totalCol = row.querySelector('.total-col');
            
            const cantidad = parseFloat(cantidadInput.value) || 0;
            const precio = parseFloat(precioInput.value) || 0;
            const totalFila = cantidad * precio;
            
            if (totalCol) totalCol.textContent = formatCurrency(totalFila);
            totalGeneral += totalFila;
        });
        document.getElementById('total-general').textContent = formatCurrency(totalGeneral);
    }

    tableBody.addEventListener('input', function(e) {
        if (e.target.classList.contains('item-calc')) updateTotals();
    });

    tableBody.addEventListener('click', function(e) {
        if (e.target.closest('.remove-row')) {
            const rows = tableBody.querySelectorAll('tr');
            if (rows.length > 1) {
                e.target.closest('tr').remove();
                updateTotals();
            }
        }
    });

    // 🚨 ESTILO NEGRO SÓLIDO FORZADO 🚨
    const inputStyle = 'background-color: #121520 !important; color: #ffffff !important; border: 1px solid rgba(255,255,255,0.1) !important; padding: 18px 24px !important; border-radius: 12px !important; font-size: 18px !important;';

    function createRow(desc = '', cant = 1, prec = '') {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><input type="text" class="form-control" name="descripcion" placeholder="Descripción del servicio..." value="${desc}" style="${inputStyle}"></td>
            <td><input type="number" class="form-control item-calc text-center" name="cantidad" value="${cant}" min="1" style="${inputStyle}"></td>
            <td><input type="number" class="form-control item-calc" name="precio" placeholder="0.00" value="${prec}" step="0.01" min="0" style="${inputStyle}"></td>
            <td class="total-col text-info fw-bold" style="vertical-align: middle; padding-left: 15px; font-family: \'Bebas Neue\'; font-size: 24px;">${formatCurrency((cant * (prec || 0)))}</td>
            <td style="vertical-align: middle;"><button type="button" class="btn btn-sm btn-outline-danger border-0 remove-row"><i class="bi bi-trash fs-4"></i></button></td>
        `;
        return row;
    }

    function initTable() {
        tableBody.innerHTML = '';
        tableBody.appendChild(createRow());
        updateTotals();
    }

    document.getElementById('add-row-btn').addEventListener('click', function() {
        tableBody.appendChild(createRow());
        hideDownloadButtons();
    });

    window.agregarProducto = function(n, d, p) {
        const newRow = createRow(d, 1, p);
        tableBody.appendChild(newRow);
        const modal = document.getElementById('productosModal');
        if (modal) {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) modalInstance.hide();
        }
        updateTotals();
    };

    if (document.getElementById('fecha')) document.getElementById('fecha').valueAsDate = new Date();
    initTable();

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
                alert('Cotización Guardada Exitosamente');
                document.getElementById('pdf-download-link').href = `/descargar-pdf/${data.cotizacion_id}`;
                document.getElementById('excel-download-link').href = `/descargar-excel/${data.cotizacion_id}`;
                showDownloadButtons();
            }
        })
        .catch(error => console.error('Error:', error));
    });
});